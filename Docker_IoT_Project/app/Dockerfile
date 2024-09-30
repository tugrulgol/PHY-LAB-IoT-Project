# Raspberry Pi için uygun bir baz imaj kullanıyoruz.
FROM python:3.11-slim-buster

# Gerekli bağımlılıkları kurmak için sistem paketlerini ekliyoruz.
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini oluştur ve set et.
WORKDIR /app

# Proje dosyalarını kopyala.
COPY . .

# Python bağımlılıklarını yükle.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Uygulamayı çalıştır.
CMD ["python", "main.py"]
