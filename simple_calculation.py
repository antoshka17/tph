import eco2ai
import warnings
warnings.filterwarnings('ignore')
tracker = eco2ai.Tracker(project_name="tph", experiment_description="training the <your model> model",
                         file_name='emission.csv')

tracker.start()

