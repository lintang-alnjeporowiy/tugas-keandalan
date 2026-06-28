saya akan membuat analisis keandalan struktur kapal

analisis file paijo-v3.ipynb, dan  section_modulus.ipynb

Kurang lebih perhitungan dapat dibagi ke tiga bagian besar
1. perhitungan beban
2. perhitungan kekuatan
3. analisis keandalan

gabungkan perhitungan yang ada di kedua file menjadi satu buah notebook jupyter (main.ipynb)
untuk perhitungan kekuatan gunakan yang baru yang di section_modulus.ipynb. gunakan perhitungan yang ada di paijo-v3.ipynb untuk perhitungan beban dan analisis keandalan.

untuk perhitungan beban ada step tambahan baru, yaitu baca file swbm.csv dan Wave-Bending-Moment.csv,
baca file tersebut kemudian visualisasikan semuanya (vertikal, torsional dan horizontal), tapi yang akan digunakan adalah yang vertikal saja.
dari yang swbm cari nilai paling kecil dan paling besar, dan jadikan absolute untuk nilai yang paling besar
kemudian nilai swbm absolut tadi jumlahkan ke semua nilai vertikal wave-bending-moment yang sudah kita dapatkan lagi
jadi nanti outputnya berupa data vertikal bending moment total. kemudian analisis data beban tersebut. cari rata2 dan standard deviasinya lalu buat probability density function (PDF) unutk beban kapal.

untuk perhitugan kekuatan gunakan perhitungan yang ada di section_modulus.ipynb material sudah terbaru data modulus juga sudah terbaru. tapi akan ada pengembangan variasi baru berupa penambahan faktor korosi
Indeks | Corrosion Rate (mm/year) | Keterangan
-------|-------|------
PB | 0.05 | Pelat Botom
SB | 0.025 | Stiffener, pembujur bottom
TT | 0.05 | Deck/pelat atas
SP | 0.025 | Stiffener, pembujur deck
TS | 0.05 | Stiffener, membujur samping
SS | 0.025 | Stiffener , melintang samping
ST | 0.025 | Stiffener, membujur samping
JJ | 0.025 | Sekat, melintang

Jadi nanti di perhitungan modulus kamu tambahi kolom baru di tabel nya berupa INDEKS yang berisikan huruf tadi (PB, SB, TT, dll), dan kolom berikutnta berisi corrosion ratenya di sesuai dengan indeksnya (macam di lookup gitu)
jadi nanti yang divariasikan kekuatan modulusnya yang beruabh karena ada korosi. nanti ada kolom baru berupa lebar_aktual yang berisi perkalian dari lebar awal dikali corrosion rate dikali dengan fungsi waktu umur kapal (T), jadi nanti modulus dihitung kembali menggunakan lebar_aktual. jadi misal nanti ada 7 variasi umur kapal 0 5 10 15 20 25 30 tahun. maka nanti akan ada 7 modulus deck dan bottom yang perlu dihitung sesuai dengan umur kapal,
berikan grafik scatternya.

setelah itu langsung saja ke perhitungan keandalan hitung untuk setiap variasi tadi. standar outputnya seperti di file paijo-v3.ipynb. perbedaanya berikan grafik perbandingan nilai untuk yang safety index, dan safety factor dengan sumbu x nya berupa umur kapal dan sumbu y nya berupa safety index dan safety factor. 
dan untuk yang joint probability density function antara JPDF antara beban dan kekuatan tetap seperti biasa cuman plotnya di gabung jadi ada 3 gambar jpdf berjejer gitu misalnya.


kemudian masalah konversi satuan, karena moudlusnya uang berubahn maka kita konversi saja dari kekuatan yang MPa ke momen N.m jadi kita kalikan dengan modulus dan kalikan dengan 1 juta (10^6), jagan lupa juga faktor korosi masih dalam milimeter, jagan lupa jadikan cm dulu.