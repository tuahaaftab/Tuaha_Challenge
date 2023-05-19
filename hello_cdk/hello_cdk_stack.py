# import ec2 Construct from aws_cdk.aws_ec2


from aws_cdk import (

    Stack,

    aws_ec2 as ec2,
)

from constructs import Construct

index_html_content = """
    <html>
        <head>
            <title>Hello World</title>
        </head>
        
        <body>
            <h1>Hello World!</h1>
        </body>
    </html>
"""

class HelloCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # Create a VPC
        vpc = ec2.Vpc(self, "Vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16")
        )


        # Create a security group
        security_group = ec2.SecurityGroup(self, "SecurityGroup",vpc=vpc)
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))


        # Create an instance in the VPC
        ec2.Instance(self, "Instance",
            
            # Assign a VPC to the instance
            vpc=vpc, 
            
            # Assign an instance type
            instance_type= ec2.InstanceType("t2.micro"),
            
            # Assign an AMI
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            # machine_image=ec2.MachineImage.latest_amazon_linux2022(),

            # Assign a security group to the instance
            security_group=security_group,

            init=ec2.CloudFormationInit.from_elements(
                
                # Create a simple config file that runs a Python web server
                ec2.InitService.systemd_config_file("simpleserver",
                    command="/usr/bin/python3 -m http.server 8080",
                    cwd="/var/www/html"
                ),
                
                # Start the server using SystemD
                ec2.InitService.enable("simpleserver",
                    service_manager=ec2.ServiceManager.SYSTEMD
                ),

                # Drop an example file to show the web server working
                ec2.InitFile.from_string("/var/www/html/index.html", index_html_content))
        )
            


        # example resource
        # queue = sqs.Queue(
        #     self, "HelloCdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
