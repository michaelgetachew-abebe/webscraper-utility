import paramiko

# Function to connect to the SFTP server
def connect_sftp(hostname, username, password):
    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp

# Function to list files ordered by creation (or modification) time
def list_files_sorted_by_creation_time(sftp, remote_directory):
    files = sftp.listdir(remote_directory)  # List files in the remote directory
    file_info = []

    # Loop through files and fetch file stats
    for filename in files:
        filepath = f"{remote_directory}/{filename}"
        try:
            # Get file attributes (such as st_mtime or st_atime)
            file_attributes = sftp.stat(filepath)
            file_info.append((filename, file_attributes.st_mtime))  # Using modification time
        except Exception as e:
            print(f"Could not retrieve stats for {filename}: {e}")

    # Sort files based on modification time (st_mtime)
    sorted_files = sorted(file_info, key=lambda x: x[1])
    
    # Print the sorted list
    for filename, mtime in sorted_files:
        print(f"{filename} - {mtime}")

# Example usage
hostname = 'your_sftp_server_address'
username = 'your_sftp_username'
password = 'your_sftp_password'
remote_directory = '/path/to/remote/directory'

# Connect to the SFTP server
sftp = connect_sftp(hostname, username, password)

# List and print files sorted by modification time
list_files_sorted_by_creation_time(sftp, remote_directory)

# Close the SFTP session
sftp.close()
