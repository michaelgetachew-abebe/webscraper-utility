### README for MSISDN-IMEI Finder Deployment


#### **Table of Contents**
1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Setup Instructions](#setup-instructions)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Support](#support)

---

### **Introduction**
This project deploys a MSISDN-IMEI Finder application on a Kubernetes cluster. The application uses Flask-based APIs to provide MSISDN-IMEI mapping services. It includes a secure deployment setup with Kubernetes best practices like TLS encryption, NetworkPolicies, and internal ClusterIP for service exposure.

---

### **Features**
- API for MSISDN-IMEI lookups.
- Secure Kubernetes deployment using:
    - Resource-efficient deployment with CPU and memory limits.

---

### **Requirements**
- Kubernetes cluster (v1.22 or later recommended).
- Kubectl CLI installed and configured.
- Docker installed for containerization.
- Access to an image registry with proper credentials.

---

### **Setup Instructions**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/michaelgetachew-abebe/webscraper-utility.git
   cd src/
   ```

2. **Build the Docker Image**
   Ensure you have Docker installed and running.
   ```bash
   docker build -t your-registry/msisdn_imei_api:latest .
   ```

3. **Push the Image to a Registry**
   Authenticate with your container registry and push the image:
   ```bash
   docker push your-registry/msisdn_imei_api:latest
   ```

4. **Set Up Kubernetes Secrets**
   Create a Kubernetes secret for your container registry credentials:
   ```bash
   kubectl create secret docker-registry regcred \
     --docker-server=<your-registry-url> \
     --docker-username=<your-username> \
     --docker-password=<your-password> \
     --docker-email=<your-email>
   ```

5. **Configure TLS Certificates**
   Add your TLS certificates as a Kubernetes secret:
   ```bash
   kubectl create secret tls tls-secret \
     --cert=<path-to-cert-file> \
     --key=<path-to-key-file>
   ```

---

### **Kubernetes Deployment**

1. **Apply the Deployment and Service**
   ```bash
   kubectl apply -f deployment.yaml
   ```

2. **Verify Deployment**
   Ensure the pods are running:
   ```bash
   kubectl get pods
   ```

3. **Verify Service**
   Check that the service is created:
   ```bash
   kubectl get svc
   ```

4. **Access the Application**
   - Use the hostname defined in the Ingress 
   - Ensure DNS is configured to resolve the hostname to your Ingress IP.

---

### **Configuration**
Update the following in the `deployment.yaml` and `ingress.yaml`:
- **Container Image**: Replace `container-registry-artifact-url:latest` with your Docker image.
- **TLS Secret**: Replace `tls-secret` with the name of your TLS secret.
- **Hostnames**: Replace `configured-host-ingress` with your desired hostname.

---

### **Usage**
- The application exposes a Flask API on port `5000`.
- Use tools like `curl` or Postman to send requests to the deployed API.

Example:
```bash
curl -X POST https://configured-host-ingress/api/v1/find-imei \
  -H "Content-Type: application/json" \
  -d '{"msisdn": "1234567890"}'
```

---

### **Support**
If you encounter issues, please contact:
- **Maintainer**: [Michael Getachew Abebe]
- **Email**: [mikygetyos@gmail.com]

Alternatively, create an issue on the GitHub repository.
