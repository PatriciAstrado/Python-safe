import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.animation as animation

def update_plot(frame_actual, z, plot):
    plot[0].remove()  # Eliminamos el plot anterior
    plot[0] = ax.plot_surface(x, y, z[:,:,frame_actual], cmap="magma") #cremamos un nuevo plot con los nuevos datos

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
try:
    N = int(input('Por favir introdusca un valor que evaluar el dominio , (default = 14)'))
except ValueError:
    N = 14

nmax = 30 #fps
x = np.linspace(-4, 4, N+1)
x, y = np.meshgrid(x, x)
z = np.zeros((N+1, N+1, nmax))

# f:(x,y) = sen(x)*cos(y)
f = lambda x, y, phase: (np.sin(x - phase) * np.cos(y - phase))   # funcion evaluada ajustada para que se mueva pro frame

for i in range(nmax):
    z[:,:,i] = f(x, y, i * 2 * np.pi / nmax)  # actualizamos los datos por cada frame 
 
plot = [ax.plot_surface(x, y, z[:,:,0], color='0.75', rstride=1, cstride=1)]
ax.set_zlim(0, 1.5)
animate = animation.FuncAnimation(fig, update_plot, nmax, fargs=(z, plot))
plt.show()


#referencia:
#https://stackoverflow.com/questions/45712099/updating-z-data-on-a-surface-plot-in-matplotlib-animation