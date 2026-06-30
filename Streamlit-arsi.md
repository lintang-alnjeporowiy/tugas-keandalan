# Rancangan Program Kalkulasi Keandalan di Streamlit

## Alur Jalan Program

1. Pengguna memasukkan nilai modulus kapal yang ingin digunakan (beri keterangan dalam m3)
2. Pengguna memasukkan nilai data material kapal
    - ada form berisi keterangan material (nama)
    - bisa upload file csv (dianggpa keterangan kekuatan MPa)
    - atau memasukkan rata2, dan atau std dev atau kovarian (pilih salah satu) dan jenis distribusi (weibull, normal, lognormal) (tambahkan parameter lain yang diperlukan untuk setiap distribusinya jika perlu)
    - bisa memasukkan lebih dari 1 jenis material jadi nanti bisa menghitung keandalan untuk setiap variasi materialnya
3. Penguna memasukkan nilai ekstrem still water bending moment  Newton Meter atau Mega Newton Meter (bisa pilih)
    - bisa memasukkan lebih dari 1 nilai untuk variasi juga yang nanti akan dianalisis
4. Pengguna memasukkan nilai eketrem Static wave Bending Moment dalam Newton Meter atau Mega Newton Meter (bisa pilih)
    - atau upload csv (stauan Newton Meter) yang nanti kamu olah unutk dapat nilai ekstrem
    - bisa memasukkan lebih dari 1 nilai untuk variasi juga yang nanti akan dianalisis
5. Pengguna memasukkan (nilai dynamic) wave bending moment
    - untuk formnya berisi (yang pasti ada untuk setiap variasinya) ketinggian gelombang (m), arah datang gelombang, dan Keterangan
    - kemudian jika pengguna ingin upload csv ada pilihan distrivusi data yang ingin digunanakn untuk memodelkan (normal, rayleigh, weibull) (tambahkan parameter yang diperlukan dalam form)
    - jika pengguna ingin memasukkan data jadi maka berikan pilihan model distrivusi yang ingin digunakan kemudian formnyua menysuaiakn parameter apa yang dibutuhkan (misal mean dan std.dev)
6. Sebelum masuk ke analilsis keandalan pengguna diberikan checlist dari semua variasi yang ingin dilakukan analsisi
7. diberikan tombol untuk memulai analisis, dilakuakann analsisi sesusi dengan variasi yang dipilih perhitungan sesuai model yang sudah kita kerjakan
8. kemudian setelah itu diberikan checklist grafiknya yang ingin ditampilkan (dumuali dari visualasisi data yang dimuasukkan, hasil olahan data (beban total) sampai JPDF)
9. diberikan tabel ringkasan semua varaisi
    
    

## Keteragnan penting

1. asumsi format file csv sama seperti sama yang saat ini digunakan atau headerless tapi letak kolomya sama, jangan lupa berikan keteranagan file csv yang diterima di setiap bagian yang menerima masukan upload file csv
2. Untuk form2 nilai ynag bisa diberikan variasi (lebih dari 1 Nilai), jika belum ada pembedanya berikan form "Keterangan" ssebagai pembeda 
