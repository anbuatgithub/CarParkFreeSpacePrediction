
def concatenate():
    X_train_augmented , Y_train_augmented = augmentation(X_train,Y_train) # data augmentation
    to_gif(vid) # checking generated augmented video
    # concatenating augmented data
    train_X = np.concatenate((X_train, X_train_augmented), axis=0)
    train_y = np.concatenate((Y_train, Y_train_augmented), axis=0)
    return train_X, train_y