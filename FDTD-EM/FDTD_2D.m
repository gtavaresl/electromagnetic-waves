clear;

% Simulation parameters
Nd = 100;
Nt = 200;

% Constants
mi = pi*4e-7;
c = 3e8; % speed of light
epsilon = 1/(mi*(c^2));
f = 3e7;% frquency in Hz
lambda = c/f;
delta = lambda/10;

% Courant constant of stability
S = 2^-0.5;
%S = S*1.0005;
dt = S*delta/c;

% Grid Dimensions
steps = Nd+1;
x = 0:delta:Nd;
y = 0:delta:Nd;

% Position of source
xsource = floor(Nd/2);
ysource = floor(Nd/2); 

% Initialization of field vectors
Ez = zeros(steps,steps);
Hx = zeros(steps,steps);
Hy = zeros(steps,steps);

% Electric Conductivity
sigma = ones(steps,steps);

k = 4e-6;
%k = 0;
for i = 1:steps
    for j = 1:steps
        sigma(i,j) = k*(((i-xsource)^2+(j-ysource)^2)^0.5);
    end
end

% FDTD Parameters
Ca= (2*epsilon-dt*sigma)./(2*epsilon+dt*sigma);
Cb = ((2*dt)/delta)./(2*epsilon+dt*sigma);
D = dt/(mi*delta);

V = VideoWriter('sim-2D-sigma.mp4','MPEG-4');
open(V);

for n = 1 : Nt
    %% FDTD
    Hx(1:steps-1,1:steps) = Hx(1:steps-1,1:steps) - D*(Ez(2:steps,1:steps) - Ez(1:steps-1,1:steps));     
    Hy(1:steps,1:steps-1) = Hy(1:steps,1:steps-1) + D*(Ez(1:steps,2:steps) - Ez(1:steps,1:steps-1));  
    Ez(2:steps,2:steps) = Ca(2:steps,2:steps).*Ez(2:steps,2:steps) + Cb(2:steps,2:steps).*((Hy(2:steps,2:steps) - Hy(2:steps,1:steps-1)) - (Hx(2:steps,2:steps) - Hx(1:steps-1,2:steps)));
    %% boundary condition
    % in x-direction
    Ez(:,1)= 0;
    Ez(:,steps) = 0;
    Hy(:,steps) = Hy(:,steps-1);
    
    % in y-direction
    Ez(1,:)= 0;
    Ez(steps,:) = 0;
    Hx(steps,:) = Hx(steps-1,:);
    %% Source
    pulse = sin(2*pi*f*n*dt);
    %pulse = heaviside(n*dt)-heaviside((n-10)*dt);
    Ez(ysource,xsource) = pulse;
    
    %% Plotting Ez-wave
    mesh(x,y,Ez,'linewidth',2);
    xlabel('X \rightarrow');
    ylabel('\leftarrow Y');
    zlabel('E_z \rightarrow');
    titlestring=['\fontsize{10}Ez(X,Y) at time step =',num2str(n)];
    title(titlestring,'color','k');
    axis([0 Nd 0 Nd -1 1]);
    %goodplot()
    
    F = getframe(gcf);
    writeVideo(V,F);

end

close(V);