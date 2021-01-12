class Config:

    method_feature = "/home/qmy/Data/MethodFeature/"
    slice_feature = "/home/qmy/Data/SliceFeature/"
    original_label = "/home/qmy/Data/label.csv"
    slice_label = "/home/qmy/Data/slice_label1.csv"
    slice_handle_label = "/home/qmy/Data/slice_label2.csv"
    output_dir = "/home/qmy/Data/"
    category_dir = "/home/qmy/Data/CategoryResult/"
    run_time = 10
    category_list = ["cmdi", "crypto", "hash", "sqli", "pathtraver", "weakrand", "securecookie", "trustbound",
                     "xpathi", "xss", "ldapi"]
    study_list = ["cmdi", "sqli", "xpathi", "xss", "ldapi"]