## Install with docker

### 1. Start docker

### 2. Build the image

```bash
docker build -t backend_xdomain .
```

### 3. Run the image

```bash
docker run -p 8000:80 backend_xdomain
```

### 4. Test the api in your browser

http://localhost:8000/docs