from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os

def process_nutritional_data_from_azurite():
    # Use Azurite development storage connection string
    connect_str = "UseDevelopmentStorage=true"

    # Force API version compatible with Azurite
    blob_service_client = BlobServiceClient.from_connection_string(
        connect_str,
        api_version="2021-12-02"
    )

    container_name = "datasets"
    blob_name = "All_Diets.csv"

    # Access the blob
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Download CSV from Azurite
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))

    # Compute average macros by diet type
    avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()

    # Save results to simulated NoSQL folder
    os.makedirs("simulated_nosql", exist_ok=True)
    result = avg_macros.reset_index().to_dict(orient="records")

    with open("simulated_nosql/results.json", "w") as f:
        json.dump(result, f, indent=4)

    return "Data processed and stored successfully."

if __name__ == "__main__":
    print(process_nutritional_data_from_azurite())
