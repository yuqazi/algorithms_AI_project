SOH = 0.6
EXP_FEATURES = []
X_TRAIN = None
LIN_REG_MODEL = None
RF_MODEL = None

KEY = ""

def change_soh(new_soh):
    global SOH
    SOH = new_soh

def change_exp_features(new_features):
    global EXP_FEATURES
    EXP_FEATURES = new_features

def change_x_train(new_x_train):
    global X_TRAIN
    X_TRAIN = new_x_train

def change_lin_reg_model(new_model):
    global LIN_REG_MODEL
    LIN_REG_MODEL = new_model

def change_rf_model(new_model):
    global RF_MODEL
    RF_MODEL = new_model

def change_key(new_key):
    global KEY
    KEY = new_key