import boto3
import socket

# התחברות ל-AWS באזור us-east-1
ec2 = boto3.client("ec2", region_name="us-east-1")

print("=== AWS EC2 Smart Dashboard & Health Check ===")

# שליפת כל המכונות בחשבון
response = ec2.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        # חילוץ שם המכונה מתוך ה-Tags
        name = "No Name"
        if "Tags" in instance:
            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    name = tag["Value"]
        
        instance_id = instance["InstanceId"]
        state = instance["State"]["Name"]
        public_ip = instance.get("PublicIpAddress", None)
        
        print(f"Server Name: {name}")
        print(f"  ├── ID: {instance_id}")
        print(f"  ├── State: {state}")
        
        if public_ip:
            print(f"  ├── Public IP: {public_ip}")
            
            # בדיקת נגישות רק אם המכונה דלוקה בפועל
            if state == "running":
                try:
                    # בדיקת חיבור לפורט 22 (SSH) עם טיימאאוט של 2 שניות
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((public_ip, 22))
                    sock.close()
                    
                    if result == 0:
                        print(f"  └── Accessibility: Reachable (Port 22 is open!)")
                    else:
                        print(f"  └── Accessibility: Unreachable (Port closed / Blocked)")
                except Exception as e:
                    print(f"  └── Accessibility: Error checking ({e})")
            else:
                print(f"  └── Accessibility: Skipped (Server is not running)")
        else:
            print(f"  └── Public IP: None (No public address assigned)")
            
        print("-" * 50)