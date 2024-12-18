import os, itertools, random
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from time import sleep
from matplotlib.image import imread


def page_leaf_visualiser_body():
    """
    Create page body for leaf visualisation image montages

    - Mean average image per class
    - Difference between average healthy and average infected
    - Image montage of raw dataset

    """

    # Define model for output images source
    version = 'v6'  # change as needed

    # instruction for users
    CHECKBOX_INSTRUCTION = '\n**Click the checkbox below**\n'

    # page title
    st.title("Leaf Image Visualiser")
    st.write(
        "As part of the dataset exploration phase, this page provides a "
        "reference for observing the visual differences between **healthy** "
        "Cherry Leaves and Cherry Leaves infected with **powdery mildew** "
        "in answer to Business Requirement No.1 as defined by the client.\n"
    )
    st.write("---")
    
    st.header("Firstly, let's explore the dataset.")
    st.write("*Click the image montage checkbox to view an image montage showing a selection fo the raw dataset to see what images were used to build this model.*")
    st.write(CHECKBOX_INSTRUCTION)

    # show the image montage
    if st.checkbox("Image Montage"):
        st.write(
            "* Click the 'Create Montage' button for an image montage of "
            "healthy or infected leaves\n")
        st.info(
            "* This montage is a great way to visualise the raw collection of "
            "images used in this project to better undersand how each label's "
            "image collection is representative of its respective label.\n"

            "In short: we can see a *clear visual distinction* between healthy "
            "and infected leaves: \n"
            "* Healthy leaves appear green and uniform in color.\n"
            "* Infected leaves display a clear pattern of white powdery mildew "
            "across the surface, usually as white spots or patches.\n"
        )

        my_data_dir = 'inputs/cherry-leaves-dataset/cherry-leaves'
        labels = os.listdir(my_data_dir + '/test')
        label_to_display = st.selectbox(
            label="Select leaf type:", options=labels, index=0)
        st.write(CHECKBOX_INSTRUCTION)

        if st.button("Create Montage"):
            # Show a spinner during a process
            with st.spinner(text="Loading"):
                sleep(10)

            image_montage(dir_path=my_data_dir + '/train',
                            label_to_display=label_to_display,
                            nrows=8, ncols=3, figsize=(10, 25))


    st.write('---')

    st.header("Now an average image:")
    st.write(
        '*We have made an image for both healthy and infected leaves which* '
        '*is a mean average representation of the dataset.*\n'
        '*This can help us understand patterns better and get a big-picture look* '
        '*at what the images in our dataset from the client show.*\n'
        )
    st.write(CHECKBOX_INSTRUCTION)

    # show mean average image per class
    if st.checkbox("Show average image per class"):

        avg_var_healty = plt.imread(f"outputs/{version}/avg_var_healthy.png")
        avg_var_powdery_mildew = plt.imread(f"outputs/{version}/avg_var_powdery_mildew.png")

        st.success("**Conclusions:**")
        st.write(
            "- Whilst to the human eye, the mean variability image per label appears similar,"
            "the distinction between individual images of each class are clearly visible from the"
            "montage: patches of visible white mildew are present on infected leaves, and healthy "
            "leaves appear more consistently green in color. This should not be difficult for a machine "
            "learning model to learn. \n"
            "- It is an appropriate problem for which a CNN will be able to provide a robust solution "
            "according to the required accuracy metrics defined by the client's business requirements."

        )

        st.image(avg_var_healty, caption=f'Healthy Leaf (mean average variability)')
        st.image(avg_var_powdery_mildew, caption='Infected Leaf (mean average variability)')



    st.write('---')

    st.header("What's different between an average healthy and an average infected leaf?")
    st.write(
        "*Let's examine what the differences are by comparing the average images we saw above* "
        "*which represent a collection of either healthy or infected leaves.*\n"
        )
    st.write(CHECKBOX_INSTRUCTION)

    # show difference image between average classes
    if st.checkbox("Difference between average healthy and average infected leaves"):
        diff_between_avgs = plt.imread(f"outputs/{version}/avg_diff.png")

        st.write(
            "Whilst we can see from the image montage that there are, more "
            "often than not, clear visual differences between individual healthy "
            "and infected leaves, this difference image does not clearly show "
            "the visible differences so easily.\n"

            "It is worth noting that the leaf perimter outline is still overall present.\n"
            "This could be due to the fact that the average images are not "
            "representative of the entire dataset but a mean average.\n"
            "With this in mind, it is clear that further technical handling of the "
            "sets of images will be required to draw effective machine learning "
            "performance.\n"
        )

        st.image(diff_between_avgs, caption='Difference between average images')


    


def image_montage(dir_path, label_to_display, nrows, ncols, figsize=(15, 10)):
    """
    Generate image montage of specififed label
    Code taken directly from this repository's Jupyter Notebook:
    DataVisualisation.ipynb
    """
    sns.set_style("dark")
    labels = os.listdir(dir_path)

    # checks if your montage space is greater than subset size
    images_list = os.listdir(dir_path+ '/' + label_to_display)
    if nrows * ncols < len(images_list):
        img_idx = random.sample(images_list, nrows * ncols)
    else:
        st.warning(
            "Decrease the number of *rows* or *columns* to"
            "create your montage.\n"
            f"There are {len(images_list)} in your subset.\n"
            f"You requested a montage with {int(nrows)} rows "
            f"and {int(ncols)} columns, making {nrows * ncols} spaces")
        return

    # create list of axes indices based on nrows and ncols
    list_rows = range(0, nrows)
    list_cols = range(0, ncols)
    plot_idx = list(itertools.product(list_rows, list_cols))

    # create figure and display images
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    for x in range(0, nrows*ncols):
        img = imread(f"{dir_path}/{label_to_display}/{img_idx[x]}")
        img_shape = img.shape
        axes[plot_idx[x][0], plot_idx[x][1]].imshow(img)
        axes[plot_idx[x][0], plot_idx[x][1]].set_title(
            f"Width {img_shape[1]}px x Height {img_shape[0]}px")
        axes[plot_idx[x][0], plot_idx[x][1]].set_xticks([])
        axes[plot_idx[x][0], plot_idx[x][1]].set_yticks([])
    plt.tight_layout()

    st.pyplot(fig=fig)