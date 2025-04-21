1. **Méthode 1** :  
   Ouvrez `notice.pdf` et faites `Ctrl+A` pour voir le texte caché en blanc.  
   → Le flag apparaît : `0xECE{wh1t3_0n_wh1t3}`  

2. **Méthode 2** :  
   ```bash
   pdftotext notice.pdf - | grep "0xECE{"
