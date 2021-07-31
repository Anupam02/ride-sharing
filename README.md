# Ride Sharing Management Service

## Overview
Ride Sharing management service

## Steps to Run the Application

```
docker build -t ride-sharing-management-service:v.1.0 .
docker run --restart unless-stopped -d -p 5000:5000 --name=RIDE-SHARING-MANAGEMENT-SERVICE ride-sharing-management-service:v.1.0
```

The service will be up and running in PORT 5000

You can view the swagger documentation in <http://localhost:5000/api/doc>.

Note: This is not complete , I believe I can improve on this further, given the time, this has been done.

<p align="center">
  <img src="./swagger-ride-share.png" width="500" title="Ride Share MGMT">
</p>