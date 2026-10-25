from datasets import load_dataset_builder

def get_license_class(repo_id, token):
    ds_builder = load_dataset_builder(repo_id, token=token)
    print(ds_builder.info.features)
    license = { value:key for key, value in enumerate(ds_builder.info.features["license"].names)}
    return license
