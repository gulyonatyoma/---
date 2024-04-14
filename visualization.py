import matplotlib.pyplot as plt
from matplotlib import animation

class Visualise:

    __catcher_x : list = []
    __catcher_y : list = []
    __aim_x : list = []
    __aim_y : list = []

    def __init__(self, datas):
        self.__catcher_x = datas[0]
        self.__catcher_y = datas[1]
        self.__aim_x = datas[2]
        self.__aim_y = datas[3]

    def graphics(self, message = '', method_type = 2):
        fig, ax_draw = plt.subplots(1, 1, figsize = (10, 5))

        fig.tight_layout(w_pad = 5, h_pad = 5)

        ax_draw.plot(self.__catcher_x, self.__catcher_y, label = 'перехватчик', color = 'red')
        ax_draw.plot(self.__aim_x, self.__aim_y, label = 'цель', color = 'blue')

        if method_type == 2:
            for i , catcherx in enumerate(self.__catcher_x):
                ax_draw.plot([catcherx, self.__aim_x[i]],
                    [self.__catcher_y[i], self.__aim_y[i]], color = 'grey', linewidth = 0.3)
                
        if method_type == 3:
            for i in range(len(self.__catcher_x)):
                ax_draw.plot([50000, self.__aim_x[i]],
                    [0, self.__aim_y[i]], color = 'grey', linewidth = 0.3)
                
        ax_draw.scatter(self.__catcher_x, self.__catcher_y, c = 'black', s = 3)
        ax_draw.scatter(self.__aim_x, self.__aim_y, c = 'black', s = 3)
        ax_draw.scatter(50000, 0, c = 'black', s = 10)
        ax_draw.set_xlim([0, 100000])
        ax_draw.set_ylim([0, 40000])
        ax_draw.set_title(message, fontsize = 10)
        ax_draw.legend()

        plt.show()

    def animation(self, message = ''):
        fig, ax_anim = plt.subplots(1, 1, figsize = (10, 5))

        fig.tight_layout (w_pad = 5, h_pad = 5)

        line1 = ax_anim.plot(self.__catcher_x, self.__catcher_y,
            label='перехватчик', color = 'red')[0]
        line2 = ax_anim.plot(self.__aim_x, self.__aim_y, label='цель', color = 'blue')[0]

        ax_anim.set_xlim([0, 100000])
        ax_anim.set_ylim([0, 40000])
        ax_anim.set_title(message, fontsize = 10)
        ax_anim.legend()

        def update(frame):
            line1.set_xdata(self.__catcher_x[:frame])
            line1.set_ydata(self.__catcher_y[:frame])
            line2.set_xdata(self.__aim_x[:frame])
            line2.set_ydata(self.__aim_y[:frame])
            return (line1, line2)
        
        anim = animation.FuncAnimation(fig=fig, func=update, frames=200, interval=50)
        plt.show()
        