# deployement.py
import os
import tarfile
import boto3
import sagemaker
from sagemaker.pytorch import PyTorchModel  # On garde PyTorchModel pour l’entry_point

# -------------------------------
#  Configuration de base
# -------------------------------
role = sagemaker.get_execution_role()
session = sagemaker.Session()
bucket = session.default_bucket()

# -------------------------------
# : Préparer le modèle pour SageMaker
# -------------------------------
model_dir = "model_package"
os.makedirs(model_dir, exist_ok=True)

# Si tu as des fichiers FAISS ou embeddings, mets-les ici
# Exemple : copie de ton index FAISS
faiss_index_path = "/tmp/faiss_index"  # dossier local contenant index.faiss + index.pkl
if os.path.exists(faiss_index_path):
    for file in os.listdir(faiss_index_path):
        full_path = os.path.join(faiss_index_path, file)
        if os.path.isfile(full_path):
            dest = os.path.join(model_dir, file)
            os.system(f"cp {full_path} {dest}")
else:
    # Création d’un fichier placeholder si pas d’index
    with open(os.path.join(model_dir, "placeholder.txt"), "w") as f:
        f.write("placeholder for SageMaker model data")

# Création du tar.gz pour SageMaker
model_tar = "legal-agent-model.tar.gz"
with tarfile.open(model_tar, "w:gz") as tar:
    tar.add(model_dir, arcname=".")

# -------------------------------
# 🪣 Étape 2 : Upload du modèle sur S3
# -------------------------------
s3_client = boto3.client("s3")
s3_key = f"legal_agent/{model_tar}"
s3_path = f"s3://{bucket}/{s3_key}"
s3_client.upload_file(model_tar, bucket, s3_key)
print(f"✅ Modèle uploadé sur S3 : {s3_path}")

# -------------------------------
# 📦 Étape 3 : Créer le modèle SageMaker
# -------------------------------
model = PyTorchModel(
    entry_point="inference.py",       # script d'inférence
    role=role,
    framework_version="2.2.0",        # PyTorch container
    py_version="py310",               # Python 3.10+
    model_data=s3_path,               
    source_dir=".",                   
    sagemaker_session=session
)

# -------------------------------
# Déployer le modèle
# -------------------------------
endpoint_name = "legal-agent-endpoint-9"

try:
    predictor = model.deploy(
        initial_instance_count=1,
        instance_type="ml.m5.large",
        endpoint_name=endpoint_name
    )
    print("\n Endpoint déployé avec succès !")
    print(f"Nom de l’endpoint : {predictor.endpoint_name}")

except Exception as e:
    print("\n Erreur lors du déploiement :")
    print(str(e))
    print("\n Vérifie les logs dans CloudWatch :")
    print(f"   Console AWS → CloudWatch → Log groups → /aws/sagemaker/Endpoints/{endpoint_name}")
