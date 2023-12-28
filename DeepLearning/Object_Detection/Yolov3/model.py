import torch
import torch.nn


#Tuple: (out_channels, kernel_size, stride)
#List: ["B", 1] -> B: Residual Block, 1: Number of repeats
#darknet architecture
darknet = [
    (32, 3, 1),
    (64, 3, 2),
    ["B", 1],
    (128, 3, 2),
    ["B", 2],
    (256, 3, 2),
    ["B", 8],
    (512, 3, 2),
    ["B", 8],
    (1024, 3, 2),
    ["B", 4] #To this point is Darknet-53
    (512, 1, 1),
    (1024, 3, 1),
    "S", #S: Scale Prediction -> Predicts the scale of the object
    (256, 1, 1),
    "U", #U: Upsample -> Upsample the feature map from the previous layer
    (256, 1, 1),
    (512, 3, 1),
    "S",
    (128, 1, 1),
    "U",
    (128, 1, 1),
    (256, 3, 1),
    "S"
]

class CNNBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels, bn_act=True, **kwargs): #bn_act: Batch Normalization and Activation
        super().__init__()
        self.conv = torch.nn.Conv2d(in_channels, out_channels, bias=not bn_act, **kwargs) #bias: if bn_act is true, bias is false if bn_act is present bias is unnecessary
        self.bn = torch.nn.BatchNorm2d(out_channels)
        self.leaky = torch.nn.LeakyReLU(0.1)
        self.use_bn_act = bn_act

    def forward(self, x):
        if self.use_bn_act:
            return self.leaky(self.bn(self.conv(x)))
        else:
            return self.conv(x)

class ResidualBlock(torch.nn.Module):
    def __init__(self, channels, use_residual=True, num_repeats=1): #num_repeats: number of times the block is repeated
        super().__init__()
        self.layers = torch.nn.ModuleList()
        for repeat in num_repeats:
            self.layers += [
                CNNBlock(channels, channels // 2, kernel_size=1), 
                CNNBlock(channels/2, channels, kernale_size=3, padding=1)
            ]

        self.use_residual = use_residual #If true, the residual block is used
        self.num_repeats = num_repeats #Number of times the block is repeated
    
    def forward(self, x):
        for layer in self.layers:
           x = layer(x) + x if self.user_residual else layer(x) #If use_residual is true, the residual block is used else the block is not used
        return x

class ScalePrediction(torch.nn.Module):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.pred = nn.Sequential(
            CNNBlock(in_channels, 2 * in_channels, kernel_size=3, padding=1),
            CNNBlock(2*in_channels, 3*(num_classes + 5), bn_act=False, kernale_size=1) #5: x, y, w, h, confidence
        )
        self.num_classes = num_classes

    def forward(self, x):
        return (
            self.pred(x)
            .reshape(x.shape[0], 3, self.num_classes + 5, x.shape[2], x.shape[3])
            .permute(0, 1, 3, 4, 2)
        )
        #N x 3 x 13 x 13 x 5+num_classes

class Yolov3(torch.nn.Module):
    def __init__(self, in_channels, num_classes=20):
        super().__init__()
        self.num_classes = num_classes
        self.in_channels = in_channels
        self.layers = self._create_conv_layers()

    def forward(self, x):
        outputs = [] #Stores the outputs of the scale prediction layers
        route_connections = [] #Stores the outputs of the residual blocks

        for layer in self.layers:
            if isinstance(layer, ScalePrediction):
                outputs.append(layer(x)) #Append the output of the scale prediction layer
                continue #Skip the rest of the loop and go to the next iteration

            x = layer(x) #Pass the input through the layer
            if isinstance(layer, ResidualBlock) and layer.num_repeats == 8: #If the layer is a residual block with 8 repeats
                route_connections.append(x) #Append the output of the residual block

            elif isinstance(layer, torch.nn.Upsample):
                x = torch.cat([x, route_connections[-1]], dim=1) #Concatenate the output of the previous layer with the output of the residual block
                route_connections.pop() #Remove the output of the residual block from the list

        return outputs

    def _create_conv_layers(self):
        layers = nn.ModuleList()
        in_channels = self.in_channels

        for module in darknet:
            if isinstance(module, tuple):
                out_channels, kernale_size, stride = module
                layers.append(CNNBlock(
                    in_channels,
                    out_channels,
                    kernale_size=kernale_size,
                    stride=stride,
                    padding=1 if kernale_size == 3 else 0,
                ))
                in_channels = out_channels #The output of the previous layer is the input of the next layer
            elif isinstance(module, list):
                num_repeats = module[1]
                layers.append(ResidualBlock(in_channels, num_repeats=num_repeats))

            elif isinstance(module, str):
                if module == "S":
                    layers += [
                        ResidualBlock(in_channels, use_residual=False, num_repeats=1),
                        CNNBlock(in_channels, in_channels//2, kernale_size=1),
                        ScalePrediction(in_channels//2, num_classes=self.num_classes)
                    ]
                elif module == "U":
                    layers.append(torch.nn.Upsample(scale_factor=2))#Upsample the feature map from the previous layer
                    in_channels = in_channels * 3 #concatenate after upsampling

        return layers