terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Security group
resource "aws_security_group" "calendar_app" {
  name        = "calendar-app-sg"
  description = "Security group for 365 Calendar App"
  
  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    description = "App port"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "calendar-app-sg"
  }
}

# EC2 instance
resource "aws_instance" "calendar_app" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 in us-east-1
  instance_type = "t2.micro"
  
  vpc_security_group_ids = [aws_security_group.calendar_app.id]
  key_name               = "calendar-key"  # Your SSH key name
  
  # User data - runs on first boot
  user_data = <<-EOF
              #!/bin/bash
              
              # Log everything
              exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
              
              echo "=== Starting 365 Calendar App Deployment ==="
              
              # Update system
              yum update -y
              
              # Install dependencies
              yum install -y docker git python3 python3-pip
              
              # Start Docker
              systemctl start docker
              systemctl enable docker
              
              # Clone your GitHub repo
              cd /home/ec2-user
              git clone https://github.com/arulraj/365-calendar.git
              cd 365-calendar
              
              # Install Python dependencies
              pip3 install -r requirements.txt
              
              # Create systemd service
              cat > /etc/systemd/system/calendar-app.service << 'SERVICE'
              [Unit]
              Description=365 Calendar Flask App
              After=network.target
              
              [Service]
              User=ec2-user
              WorkingDirectory=/home/ec2-user/365-calendar
              ExecStart=/usr/bin/python3 /home/ec2-user/365-calendar/app.py
              Restart=always
              
              [Install]
              WantedBy=multi-user.target
              SERVICE
              
              # Start the service
              systemctl daemon-reload
              systemctl enable calendar-app
              systemctl start calendar-app
              
              # Also run in Docker (optional)
              if [ -f "Dockerfile" ]; then
                docker build -t calendar-app .
                docker run -d -p 5000:5000 --name calendar-app-docker calendar-app
              fi
              
              # Create update script
              cat > /home/ec2-user/update-app.sh << 'SCRIPT'
              #!/bin/bash
              cd /home/ec2-user/365-calendar
              git pull origin main
              systemctl restart calendar-app
              echo "App updated at \$(date)"
              SCRIPT
              
              chmod +x /home/ec2-user/update-app.sh
              
              echo "=== Deployment Complete ==="
              echo "App will be available at: http://\$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5000"
              echo "Update with: ./update-app.sh"
              EOF

  tags = {
    Name = "365-calendar-app"
  }
}

# Output
output "app_url" {
  value = "http://${aws_instance.calendar_app.public_ip}:5000"
}

output "ssh_command" {
  value = "ssh -i ~/calendar-key.pem ec2-user@${aws_instance.calendar_app.public_ip}"
}

output "deployment_commands" {
  value = <<-EOT
  
  🎉 DEPLOYMENT COMPLETE!
  
  Your app is running at: http://${aws_instance.calendar_app.public_ip}:5000
  
  Test it:
  curl http://${aws_instance.calendar_app.public_ip}:5000/api/health
  curl http://${aws_instance.calendar_app.public_ip}:5000/api/days
  
  SSH to server:
  ssh -i ~/calendar-key.pem ec2-user@${aws_instance.calendar_app.public_ip}
  
  Update app manually:
  ssh -i ~/calendar-key.pem ec2-user@${aws_instance.calendar_app.public_ip} ./update-app.sh
  
  EOT
}