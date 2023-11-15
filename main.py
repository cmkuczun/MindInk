from backend.classifier.predict import get_model, query_sd_api, get_prompt, predict
# from frontend.ui import on_button_click

# main body flow
def main():
    pass


# test control flow with hardcoded inputs (do not ask for user input)
def test():
    # TODO: make API calls work!!

    # get the test image
    test_img_path = "/Users/claudia/ai-proj-mindink/MindInk/rose-test.png"
    model = get_model()
    print("got model")
    res = predict(test_img_path,model)
    print(res)



if __name__ == "__main__":
    test()
    #main()




