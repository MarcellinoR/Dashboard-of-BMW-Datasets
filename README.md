🚗 BMW Business Intelligence & Price Predictor

📌 Overview

Proyek ini adalah dashboard **Business Intelligence (BI)** interaktif yang dirancang khusus untuk menganalisis ekosistem data kendaraan BMW. Selain menyediakan visualisasi tren penjualan, dashboard ini dilengkapi dengan fitur **Smart Price Predictor** menggunakan pendekatan statistika untuk mengestimasi harga jual kendaraan.

📊 Fitur Analisis Statistika

Dalam repository ini, saya menerapkan beberapa konsep statistika dan data science:

1.  **Multiple Linear Regression**: Fitur prediksi harga menggunakan variabel *mileage* (jarak tempuh), *year* (tahun), dan *engineSize* (kapasitas mesin) untuk menghitung estimasi harga jual secara objektif.
      * **Persamaan:** $Y = \beta_0 + \beta_1X_1 + \beta_2X_2 + \beta_3X_3 + \epsilon$
2.  **Correlation Heatmap**: Analisis multivariat untuk melihat hubungan antar variabel teknis (seperti pengaruh `mpg` terhadap `price` atau `engineSize` terhadap `tax`).
3.  **Distribution Analysis**: Menggunakan histogram dan donut chart untuk memahami komposisi transmisi dan jenis bahan bakar (Fuel Type) yang paling dominan di pasar.

## 🛠️ Stack Teknologi

  * **Frontend & Dashboard:** Streamlit (dengan kustomisasi CSS Dark Mode).
  * **Data Visualization:** Plotly Express & Graph Objects (Interaktif).
  * **Machine Learning:** Scikit-Learn (Linear Regression).
  * **Database Management:** SQLAlchemy & PyMySQL untuk koneksi database relasional.

## 🚀 Cara Menjalankan

1.  **Clone Repository:**
    ```bash
    git clone https://github.com/MarcellinoR/Dashboard-of-BMW-Datasets.git
    cd Dashboard-of-BMW-Datasets
    ```
2.  **Install Library:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Konfigurasi Database:**
    Pastikan MySQL Anda menyala dan memiliki database bernama `Car` dengan tabel `bmw`. Sesuaikan *connection string* di `app.py` jika diperlukan.
4.  **Run Dashboard:**
    ```bash
    streamlit run app.py
    ```

## 📂 Struktur Folder

  * `bmw.py`: Script utama dashboard dan logika machine learning.
  * `.gitignore`: Mengabaikan file *cache* dan *virtual environment*.
  * `requirements.txt`: Daftar dependensi library Python.

-----


**Apakah ada bagian lain dari repository ini yang ingin Anda poles sebelum melakukan *push* pertama ke GitHub?**
