import os
from folder_paths import get_filename_list, get_full_path
import comfy.sd

class EichenLoopModelSelector:
    @classmethod
    def INPUT_TYPES(cls):
        model_list = get_filename_list("diffusion_models")
        optional_inputs = {}
        for i in range(1, 11):
            if not model_list:
                optional_inputs[f"model_{i}"] = (model_list, {})
            else:
                default_index = (i - 1) % len(model_list)
                optional_inputs[f"model_{i}"] = (model_list, {"default": model_list[default_index]})
        return {
            "required": {
                "number_of_models": ("INT", {"default": 3, "min": 1, "max": 20, "step": 1}),
            },
            "optional": optional_inputs
        }

    RETURN_TYPES = ("MODEL", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("model", "model_path", "model_name", "model_folder")
    FUNCTION = "select_models"
    CATEGORY = "Eichen"
    OUTPUT_IS_LIST = (True, True, True, True)

    def select_models(self, number_of_models, **kwargs):
        available_models = [
            kwargs[f"model_{i}"] for i in range(1, number_of_models + 1)
            if f"model_{i}" in kwargs and kwargs[f"model_{i}"]
        ]
        if not available_models:
            raise ValueError("No models selected. Please ensure at least one model is selected.")
        models = []
        model_paths = []
        model_names = []
        model_folders = []
        for selected_model in available_models:
            model_name = os.path.splitext(os.path.basename(selected_model))[0]
            model_path = get_full_path("diffusion_models", selected_model)
            model_folder = os.path.basename(os.path.dirname(model_path))
            model = comfy.sd.load_diffusion_model(model_path)
            models.append(model)
            model_paths.append(model_path)
            model_names.append(model_name)
            model_folders.append(model_folder)
        return (models, model_paths, model_names, model_folders)
