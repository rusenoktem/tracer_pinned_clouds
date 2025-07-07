make_fig4.m
function dKE = make_fig4(beta,sonde_path)
% dKE calculates 
%
% Inputs:
%   beta       : Constant for turbulent kinetic energy calculation.
%   sonde_path :
% Outputs:
%   dKE        : The final calculated vertical velocity, which will be
%
% Global Variables:
%   Ttrip  : Triple point temperature of water (K).
%   cpa    : Specific heat of dry air at constant pressure (J/kg/K).
%   ggr    : Acceleration due to gravity (m/s^2).
global Ttrip;
global cpa;
global ggr;

Ttrip = 273.16;     % K
ggr   = 9.81;       % m/s^2
cpa   = 1006;       % J/kg/K

%load list of days independently classified by two authors as 
%-1 (no surface rooted clouds),
% 0 (indecisive),  
% 1 (surface-rooted clouds) and pinned clouds
load ../Data/tracer_cloud_classes.mat 
N = size(tracer_cloud_classes.date,1);

%calculate smallest non-negative w(zo), z>= zo and z <= zLCL
for j = 1:N,
    %read sonde for the corresponding date
    dtstr = tracer_cloud_classes.date(j,:);
    flist = dir(strcat(sonde_path,'housondewnpnM1.b1.',dtstr,'.11*.cdf'));
    if isempty(flist)
        fprintf('warning: no sonde data for %s--skipping\n',dtstr);
        continue;
    end
    fname = strcat(flist(1).folder,'/',flist(1).name);
    sonde = read_sonde_data(fname);
    sonde.T = sonde.tdry + Ttrip;
    
    %find the height index for the surface (100 m)  
    z0 = find(abs(sonde.alt-100) == min(abs(sonde.alt-100))); z0 = z0(end);

    %calculate LCL
    zLCL = lcl(sonde.p(z0)*100,sonde.T(z0),sonde.rh(z0)*1e-2,0,0)+sonde.alt(z0);

    %find the height index for zLCL 
    ze = find(abs(sonde.alt-zLCL) == min(abs(sonde.alt-zLCL))); ze = ze(end);
    
    [rv(j),fv(j)] = root_solve(sonde,z0,ze,beta);
end

dKE = .5*(fv.^2-(rv).^2);
plot_hist(dKE,tracer_cloud_classes);
end


function wout = calc_wo_non_neg(sonde,z0,ze,beta)
global Ttrip;
global cpa;
global ggr;

    wout = [0 0 ze];
    if (ze > z0) % continue if zLCL (ze) is greater than z1, otherwise return 0 
        se_z = cpa*sonde.T(z0:ze+1) + ggr*sonde.alt(z0:ze+1); %dry static energy 
        b_z = ggr*(se_z(1)-se_z)./sonde.T(z0:ze+1)/cpa; 
        du = abs(diff(sonde.uw(z0:ze+1))) + abs(diff(sonde.vw(z0:ze+1))); %wind shear
        dz = diff(sonde.alt(z0:ze+1));
        tke = beta*du./dz;
        for w0 = 1e-5:0.1:50                    %vary w_0 from 0 to find the minimum
            wz = w0;                             %step 0
            wz = wz + dz(1)*tke(1);              %step 1, bi = 0
            for z = 2:length(du)-1               %continue up to LCL
                wzp = wz + dz(z)*(b_z(z)/wz + tke(z)); 
                %exit if w(z+1) < 0
                if (wzp <= 0)
                    break;
                else
                    wz = wzp;
                end
            end
            if (z==length(du)-1) 
                wout = [w0 wzp ze];
                break;
            end
        end
    else
        fprintf('warning: too low LCL \n')
    end
    
    if (wout(1) == 0 & wout(2) == 0)
        fprintf('could not find min w0 \n')
    end

end




function wz = evalf(w0, sonde, z0, ze, beta)
% EVALF calculates a modified vertical velocity (wz) based on atmospheric
% sounding data and an initial vertical velocity (wo).
%
% Inputs:
%   wo     : Initial vertical velocity component.
%   sonde  : Structure containing sounding data with fields:
%            .T   (Temperature in K, array)
%            .alt (Altitude in meters, array)
%            .uw  (U-component of wind in m/s, array)
%            .vw  (V-component of wind in m/s, array)
%   z0     : Starting index for the sounding data arrays.
%   ze     : Ending index for the sounding data arrays (inclusive, refers
%            to the index of sonde.T(ze+1) and sonde.alt(ze+1)).
%   beta   : Constant for turbulent kinetic energy calculation.
%
% Outputs:
%   wz     : The final calculated vertical velocity, which will be

global Ttrip;
global cpa;
global ggr;

        se_z = cpa*sonde.T(z0:ze+1) + ggr*sonde.alt(z0:ze+1); %dry static energy 
        b_z = ggr*(se_z(1)-se_z)./sonde.T(z0:ze+1)/cpa; 
        du = abs(diff(sonde.uw(z0:ze+1))) + abs(diff(sonde.vw(z0:ze+1))); %wind shear
        dz = diff(sonde.alt(z0:ze+1));
        tke = beta*du./dz;
        wz = w0 + dz(1)*tke(1);              %step 1, bi = 0
        for z = 2:length(du)-1               %continue up to LCL
                wz = wz + dz(z)*(b_z(z)/wz + tke(z)); 
                %exit if w(z+1) < 0
                if (wz <= 0 )
                    wz = 1e10;
                    break;
                end
        end            
end

function [rv,fval] = root_solve(sonde, z0, ze, beta)

    objective_function = @(wo_val) evalf(wo_val, sonde, z0, ze, beta);
    wo = 0;%1e-5;
    sI = [wo 50];
    [rv,fval] = fminbnd(objective_function,wo,50);

end

function plot_hist(y,l)
    bin_length = 2; clf;
    bins = (-139:bin_length:140);
    %no-surface rooted clouds
    lind = find(l.label1 < 0 & l.label2 < 0 & l.pinned == 0);
    h = histogram(y(lind),bins);
    h1 = h.Values;

    %surface rooted clouds
    lind = find(l.label1 > 0 & l.label2 > 0 & l.pinned == 0);
    h = histogram(y(lind),bins);
    h2 = h.Values;

    %pinned clouds
    lind = find(l.pinned >0 );
    h = histogram([y(lind)],bins);
    h3 = h.Values;

    plot(bins(1:end-1)+bin_length/2,h1/sum(h1)/bin_length,'-','color',.6*[1 1 1],'LineWidth',2 ); hold on;    
    plot(bins(1:end-1)+bin_length/2,h2/sum(h2)/bin_length,'-','color','black','MarkerFaceColor',0*[1,1,1],'LineWidth',2 );
    plot(bins(1:end-1)+bin_length/2,h3/sum(h3)/bin_length,'-','color','red','MarkerSize',9,'MarkerFaceColor','red','LineWidth',2 );
   
    grid on;
    l = legend('No surface-rooted clouds','Surface-rooted clouds','Pinned clouds only','Interpreter','tex');
    xlim([-20 20])
    xlabel('\Delta KE (J/kg)')
    ylabel('Normalized density of mornings (kg/J)')
    [min(y) max(y)]
end

function sonde = read_sonde_data(aname)
    %SONDE
    if (~exist(aname,'file'))
        alt = 0; tdry = 0;rh = 0;
        ts = 0; p = 0;tdew = 0;
        return;
    end
    sonde.p = ncread(aname,'pres');%hPa
    sonde.tdry = ncread(aname,'tdry');
    sonde.tdew = ncread(aname,'dp');
    sonde.uw = ncread(aname,'u_wind');
    sonde.vw = ncread(aname,'v_wind');
    sonde.alt = ncread(aname,'alt');
    sonde.rh = ncread(aname,'rh');
    sonde.ts = ncread(aname,'time'); 
end
