from chembl_webresource_client.new_client import new_client
import pickle

molecule = new_client.molecule
CHEMBLID = ["CHEMBL262869","CHEMBL1644677","CHEMBL216335"]

mdic = {}
count = 1
for mid in CHEMBLID:
    print(count,"/",len(CHEMBLID))
    try:
        m = molecule.get(mid)
        mdic[mid] = m["molecule_structures"]["canonical_smiles"]
        print("success  for ",mid," : ", m["molecule_structures"]["canonical_smiles"])
        if count % 1000 == 0:
            name = "smilesData/chemblSmiles_by"+str(count)+".dump"
            with open(name,"wb") as f:
                pickle.dump(mdic,f)
    except:
        mdic[mid] = "error"
        print("error for  ",mid)
    count+=1

with open("smilesData/allSmiles.dump","wb") as f:
  pickle.dump(mdic,f)