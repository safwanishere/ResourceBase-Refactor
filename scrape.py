from pathlib import Path

Y1subs = ['AHSD02', 'AHSD03', 'AHSD07', 'ACSD01', 'AHSD09', 'ACSD02', 'AHSD05', 'AMED03', 'AHSD06', 'ACSD04', 'AHSD01', 'AHSD08', 'ACSD05', 'AEED01', 'AHSD04', 'ACSD06', 'AMED02', 'AEED03', 'ACSD03', 'AHSD10', 'AHSD01', 'AEED01', 'AHSD04', 'AMED02', 'AEED03', 'ACSD03', 'AHSD03', 'AHSD07', 'AHSD05', 'AHSD09', 'AMED03', 'ACSD04', 'AMED01', 'AMED04', 'AMED05', 'ACSD07', 'AEED02', 'AEED04']
Y2subs = ['AECD04', 'ACSD08', 'ACSD09', 'AHSD11', 'AITD01', 'ACSD10', 'ACSD11', 'AITD02', 'ACSD12', 'ACSD13', 'ACSD14', 'ACSD15', 'AITD03', 'AITD04', 'ACSD16', 'ACSD17', 'AITD05', 'ACSD18', 'ACAD01', 'ACAD03', 'ACAD04', 'ACDD01', 'ACDD03', 'ACDD04', 'ACCD01', 'ACCD02', 'ACCD03', 'AAED01', 'AAED02', 'AAED03', 'AAED04', 'AAED05', 'AAED06', 'AAED07', 'AAED08', 'AAED09', 'AAED10', 'AAED11', 'AAED12', 'AAED13', 'AHSD12', 'AECD01', 'AECD02', 'AECD03', 'AECD06', 'AECD07', 'AECD08', 'AECD09', 'AECD10', 'AECD11', 'AECD12', 'AECD14', 'AECD15', 'AECD16', 'AECD18', 'AEED05', 'AEED06', 'AEED07', 'AECD05', 'AEED08', 'AEED09', 'AEED10', 'AEED11', 'AEED12', 'AECD13', 'AHSD13', 'AEED13', 'AEED14', 'AECD17', 'AMED06', 'AMED07', 'AMED08', 'AMED09', 'AMED10', 'AMED11', 'AMED12', 'AMED13', 'AMED14', 'AMED15', 'AMED16', 'AMED17', 'AMED18', 'ACED01', 'ACED02', 'ACED03', 'ACED04', 'ACED05', 'ACED06', 'ACED07', 'ACED08', 'ACED09', 'ACED10', 'ACED11', 'ACED12', 'ACED13']


for i in Y2subs:
    dirPath = Path(f"resources/Y2/{i}")
    
    try:
        dirPath.mkdir(parents=True)
        print(f"Directory '{dirPath}' created successfully.")
    except FileExistsError:
        print(f"Directory '{dirPath}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{dirPath}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
