1. **Méthode 1** :  
   Ouvrez `notice.pdf` et faites `Ctrl+A` pour voir le texte caché en blanc.  
   → Le flag apparaît

2. **Méthode 2** :  
   ```bash
   pdftotext notice.pdf - | grep "MAC{"
