clear;

Nx = 100;
Nt = 1000;

c = 3e8;
f = 3e7;
lambda = c/f;
%dx = lambda/10;
dx = c/(Nx*f);
S = 1; % Courant constant of stability
dt = (S*dx)/c;

Ez = zeros(1,Nx);
Hy = zeros(1,Nx);

%V = VideoWriter('simulation-1D-pulse');
%open(V);

for t = 1:Nt
    % Source
    Ez(1) = sin(2*pi*f*t*dt);
    
    for k = 2:Nx-1
        Ez(k)=Ez(k)+S*(Hy(k)-Hy(k-1));
    end
    %PMC
    %Ez(Nx) = Ez(Nx-1);
    
    for k=1:Nx-1
        Hy(k)=Hy(k)+S*(Ez(k+1)-Ez(k));
    end
    % PEC
    Hy(Nx) = Hy(Nx-1);
    
    tiledlayout(2,1)
    % Top plot
    ax1 = nexttile;
    plot(Ez)
    %axis([1 Nx -4 4]);
    title('Ez')

    % Bottom plot
    ax2 = nexttile;
    plot(Hy)
    axis([1 Nx -4 4]);
    title('Hy')
    
    F = getframe(gcf);
 %   writeVideo(V,F);
end

%close(V);

function s = unit_step(t)
    s = heaviside(t)-heaviside(t-20);
end

function s = gaussian_pulse(t)
    t0=20;
    spread=2;
    s = exp(-.5*((t-t0)/spread)^2);
end