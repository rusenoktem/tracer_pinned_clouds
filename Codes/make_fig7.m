function make_fig7()
   close all
   global colors;
   colors = make_marker_colors();

   %spagetti plots
   out = load_tracking_data();
   figure('Position',[800 20 800 400]);
   plot_tracking_data(out,3,'height [km]')
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function out = load_tracking_data()
    load ../Data/track20220622.mat
    ind = [1 25;26 49;50 72; 83 95;96 115; 131 161];
    for i = 1:6,
        out{i}.xyz = data(ind(i,1):ind(i,2),5:7)/1e3; % convert to km
        out{i}.t = tmI(ind(i,1):ind(i,2))-tmI(ind(i,1));
    end

end

function out = plot_tracking_data(out,ind,ylb)
    
    for i = 1:6,
        plot(out{i}.t,out{i}.xyz(:,ind)); hold on;
    end
    xlabel('time [s]')
    ylabel(ylb)
    grid on;
end
