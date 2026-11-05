# News Evidence Engine – webbprototyp

## Lokalt

Kräver Python 3.10 eller senare. Kör `python server.py` och öppna http://127.0.0.1:8765.

Kör automatiserade tester med `python -m unittest -v`.

## Publicera med GitHub och Render

1. Skapa ett nytt repository i GitHub (helst privat) och ladda upp samtliga filer från denna mapp i roten av repositoryt, inte ZIP-filen.
2. Öppna https://dashboard.render.com/ och skapa New > Web Service.
3. Anslut ditt GitHub-repository. Render stöder en blueprint via render.yaml, eller ange manuellt:
   - Language: Python 3
   - Build Command: `python -m unittest -v`
   - Start Command: `python server.py`
   - Välj lämplig plan.
4. Skapa tjänsten och öppna Render-URL:en som visas när den är publicerad.
5. Lägg till en egen domän under Render-tjänstens inställningar om du vill.

`server.py` använder miljövariabeln PORT och lyssnar på 0.0.0.0 när PORT finns, vilket är nödvändigt för Render.

## Viktiga begränsningar

Detta är en *demonstrationsprototyp*, inte en färdig publik faktagranskningstjänst. Analysen kräver att användaren själv matar in och graderar belägg. Inga källor hämtas eller verifieras automatiskt. Resultat är modellindex, inte sannolikheten att en nyhet är sann. Inget lagras. För bred offentlig användning behövs säkerhetshärdning, rate limiting, övervakning och fördjupad metodvalidering.
