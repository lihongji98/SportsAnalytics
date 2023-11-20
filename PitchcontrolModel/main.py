import matplotlib.pyplot as plt
from PitchControl import PitchControl
from position import position


def draw_heatmap(data):
    plt.imshow(data, cmap='coolwarm', interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.title('Home_Pitch_Control')
    plt.show()


if __name__ == '__main__':
    home_info, away_info = position()
    model = PitchControl()
    model.process_frame_data(home_info, away_info)
    pc_surface = model.compute_pitchControl()
    draw_heatmap(pc_surface)


