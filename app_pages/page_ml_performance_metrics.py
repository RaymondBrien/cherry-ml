import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.image import imread
from src.machine_learning.eval import load_evaluation


def page_ml_performance_metrics():
    """
    Display ML performance page body
    Detail Train Val Test split ratios
    """
    version = 'v6' # TODO edit version if required after final training
    class_distribution = plt.imread(
        f"outputs/{version}/class_distribution.png")

    st.image(class_distribution,
             caption='Labels Distribution on Train, Validation and Test Sets')


    st.header("ML Performance Metrics")
    st.write("### Train, Validation and Test Set: Labels Frequencies")

    st.write(
        "The dataset was split into 3 sets: Train, Validation and Test according "
        "to the following ratios:\n"
        # TODO fill in missing percentages
        "* Set: % \n"
        "* Set: % \n"
        "* Set: % \n"
    )
    st.write("Dataset breakdown")
    # TODO include images representing raw balance of classes
    st.info(
        # TODO make this a DF and write total ratios
        "* Train - healthy: 1472 images\n"
        "* Train - powdery_mildew: 1472 images\n"
        "* Validation - healthy: 210 images\n"
        "* Validation - powdery_mildew: 210 images\n"
        "* Test - healthy: 422 images\n"
        "* Test - powdery_mildew: 422 images\n"
        "* **4208 images total**"
    )
    st.write("---")

    st.write("### Model History")
    st.info(
        "Detailed by the graph below, the learning cycle for this "
        "binary classification model demonstrates: "
        "* a combination of good accuracy and low loss after epoch four during training.\n"
        # TODO how many for train?
        "* As expected, given the very small dataset of X images in the train set total "
        "the small, simple model with 3 lightweight convolutional layers generalises well to the given data"
        "From the documented training accuracy and loss plots, a normal learning curve is demonstrated. \n"
        "The model is neither overfitting or underfitting.\n"

        # TODO Show model outline png
        "Early stopping was also invoked for streamlined learning, defined by accuracy metrics.\n"


    )

    # show model acc 
    model_acc = plt.imread(f"outputs/{version}/model_training_acc.png")
    st.image(model_acc, caption='Model Training Accuracy')
    
    # show model loss
    model_loss = plt.imread(f"outputs/{version}/model_training_losses.png")
    st.image(model_loss, caption='Model Training Losses')
    
    st.write("---")

    st.write("### Generalised Performance on Test Set")
    data = pd.DataFrame(
        load_evaluation(version, dataset='test'),
        index=['Loss', 'Accuracy'])
    
    # show stats df
    stats = st.dataframe(data)
    # to dynamically update text for future models
    accuracy_reading = format((data.at['Accuracy', 'test']*100), '.2f')

    st.success(
        f"**The general accuracy of ML model is {accuracy_reading}%** "
    )

    st.write("---")

    st.write("Further info:")
    st.info(
        "The ML model was trained on a dataset consisting of 4208 cherry leaves in total. "
        "Testing involved an unseen set of 422 cherry leaves, split during the data preparation phase.\n"
        f"The model achieved an accuracy of {accuracy_reading}% on the test set.\n"
        "This indicates that the model is capable of predicting the presence of powdery mildew in cherry "
        "leaves with a high degree of accuracy, and able to achieve the required performance metrics.\n"
    )

    # display validation evaluation as streamlit dataframe
    st.write('Extra Stats')
    dataset = load_evaluation(version, dataset=['val'])
    st.dataframe(pd.DataFrame(dataset, index=['Loss', 'Accuracy']))
    
    st.write(
        "It can be observed that sufficient accuracy is also present on the validation set, "
        "based on the trained model's evaluation pkls.\n"
        "These evaluations were held to observe the model during the training process for "
        "thoroughness."
        )
