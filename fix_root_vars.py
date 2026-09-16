with open('style.css', 'r', encoding='utf-8') as f:
    text = f.read()

root_vars = '''
  /* Restored missing legacy color variables */
  --navy: #0B1D3A;
  --cream: #FBF7F0;
  --stone: #E8E2D9;
  --mist: #9A9490;
  --gold: #C8962E;
  --white: #FFFFFF;
  --table-header: #EAEAEA;
  --heading-font: 'Alef', sans-serif;
  --body-font: 'Alef', sans-serif;
'''

text = text.replace('/* Restored missing color variables */', root_vars + '\n  /* Restored missing color variables */')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(text)
