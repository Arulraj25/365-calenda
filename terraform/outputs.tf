output "deployment_info" {
  value = <<-EOT
  
  🚀 DEPLOYMENT COMPLETE!
  
  Application URL: http://${aws_instance.app.public_ip}
  Health Check: http://${aws_instance.app.public_ip}/api/health
  
  SSH to server: ssh -i calendar-key.pem ec2-user@${aws_instance.app.public_ip}
  
  To update app manually:
  ssh -i calendar-key.pem ec2-user@${aws_instance.app.public_ip} ./update-app.sh
  
  EOT
}