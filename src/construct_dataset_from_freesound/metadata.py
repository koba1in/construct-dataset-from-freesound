from datasets import load_dataset_builder

def get_license_class(repo_id, license_column, token):
    ds_builder = load_dataset_builder(repo_id, token=token)
    license = { value:key for key, value in enumerate(ds_builder.info.features[license_column].names)}
    return license
