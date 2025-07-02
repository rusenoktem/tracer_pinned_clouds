close all; clear; %clear previous plots and data to avoid data conflict
figure('Position',[20 20 800 1600]);
fig_path = '../Data/';

%sx and sy are relative positions in the figure
sx = 0.05; 

%The following pictures are cropped from the originals and outlined for
%better identification of pinned clouds from the background
%The P1 P2 positions are determined by projecting the true positions using
%camera projection matrices

%cu1_outline_u.png: original image: houstereocamaS5.a1.20220513.123000.jpg
sy = 0.75; plot_panel(strcat(fig_path,'cu1_cropped_left.png'),sx,sy,'(a) 13 May 2022, 0730 LT');
%cu1_outline_u.png: original image: houstereocamaS5.a1.20220618.122000.jpg
sy = 0.5;  plot_panel(strcat(fig_path,'cu2_cropped_left.png'),sx,sy,'(c) 18 June 2022, 0720 LT');
%cu1_outline_u.png: original image: houstereocamaS5.a1.20220622.120000.jpg
sy = 0.25; plot_panel(strcat(fig_path,'cu3_cropped_left.png'),sx,sy,'(e) 22 June 2022, 0700 LT');

sx = 0.55; 
%cu1_outline_u.png: original image: houstereocamaS5.a1.20220513.143000.jpg
sy = 0.75; plot_panel(strcat(fig_path,'cu1_cropped_right.png'),sx,sy,'(b) 13 May 2022, 0930 LT');
%cu1_outline_u.png: original image: houstereocamaS5.a1.20220618.142000.jpg
sy = 0.5;  plot_panel(strcat(fig_path,'cu2_cropped_right.png'),sx,sy,'(d) 18 June 2022, 0920 LT');
%cu1_outline_u.png: original image: houstereocamaS5.a1.20220622.141000.jpg
sy = 0.25; plot_panel(strcat(fig_path,'cu3_cropped_right.png'),sx,sy,'(f) 22 June 2022, 0910 LT');

%%%%panel g%%
subplot('Position',[0.1 0.02 0.8 0.2])
%read relevant stack data from TECQ file
p_data = read_EI_data('../Data/EIData.xlsx');
plot_stack_locations(fig_path, p_data);
title('(g)')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%panels a-f %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function plot_panel(imname,sx,sy,imtitle)
    im = imread(imname);
    subplot('Position',[sx sy 0.4 0.2])
    imagesc(im); axis off;
    title(imtitle)
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function out = plot_stack_locations(fig_path, p_data)

	%map_zoom.png is extracted from Google Earth
	map = imread(strcat(fig_path,'map_zoom.png'));
	im = image(map);
	axis off;
	im.AlphaData = 0.5;
	[Y X d] = size(map);
	pbaspect([X Y 1]) %keep the aspect ratio

	%corner positions of the map to use for scaling
	     %pixelx     pixely     lat                longitude
	pos = [16         33      29+37/60+41/3600   95+4/60+9/3600 ;...
	       1585       569     29+37/60+14/3600   95+2/60+35/3600];

		                    %ground level is ~ 8 meters
	[e,n,u] = GpsToENU(pos(2,3), -pos(2,4), 8,pos(1,3), -pos(1,4),8);
	sx = (pos(2,1)-pos(1,1))/e;  %scale in x
	sy = (-pos(2,2)+pos(1,2))/n; %scale in y

	lat_lon_P1(:,1) = p_data.p1(:,2);
	lat_lon_P1(:,2) = p_data.p1(:,3);
	lat_lon_P2(:,1) = p_data.p2(:,2);
	lat_lon_P2(:,2) = p_data.p2(:,3);
	%find P1 and P2 locations in km from the upper left corner of the map
	[ep1,np1,u] = GpsToENU(lat_lon_P1(:,1), lat_lon_P1(:,2), 8,pos(1,3), -pos(1,4),8); 
	[ep2,np2,u] = GpsToENU(lat_lon_P2(:,1), lat_lon_P2(:,2), 8,pos(1,3), -pos(1,4),8);

	ep = [ep1;ep2]; np = [np1;np2]; %east, north in km
    pwr = [p_data.p1(:,4).*p_data.p1(:,6);...
           p_data.p2(:,4).*p_data.p2(:,6)];

	%find and combine stacks that are too close to each other 
	out = [];
	for i = 1:length(ep)
	    if (pwr(i))
		d = sqrt((ep-ep(i)).^2 + (np-np(i)).^2);
		ind = find(d < 0.2 & pwr >0 );
		cur = sum(pwr(ind));
		out = [out; cur mean(ep(ind)) mean(np(ind))];
		pw(ind) = 0;   
	    end
    end

	scr = 8; %just to scale for better visibility
	pwr = out(:,1)*scr; ep = out(:,2); np = out(:,3);
	hold on; %overlay
	scatter(pos(1,1)+sx*ep,pos(1,2)-sy*np,pwr,[0.1 0.1 0.7],'o','filled','MarkerFaceAlpha',.8)
	fs = 13; %fontsize 
	%overlay plants
	text(pos(1,1)+sx*ep(1)-60,pos(1,2)-sy*np(1)-65,{'P1'},'color','black','FontSize',fs, 'FontWeight','bold')
	text(pos(1,1)+sx*ep(end)-160,pos(1,2)-sy*np(end)-65,{'P2'},'color','black','FontSize',fs,'FontWeight','bold')

	%Print the legend
	line(300+[-sx*.5 0],(Y-120)*[1 1],'color','black','LineWidth',3)
	text(140,Y-155,'500 m','color','black','FontSize',fs-3,'FontWeight','bold')
	scatter(60,Y-55,(50)*scr,[0.1 0.1 0.7],'o','filled','MarkerFaceAlpha',.8)
	text(120,Y-55,'50 MW','color','black','FontSize',fs-3,'FontWeight','bold')
	%point to north
	quiver(370,Y-20,0,-100,1,'color','black','LineWidth',3,'MaxHeadSize',3)
	text(355,Y-150,'N','color','black','FontSize',fs-3,'FontWeight','bold')
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
function [e,n,u] = GpsToENU(lati, longi, alti, latr,  longr, altr)
%eastward, northward, and alt difference in km from the reference latr,
%lonr, altr. Input alti and altr must be in meters

    cosLatRad=cos(latr*pi/180);
    cosLongRad=cos(longr*pi/180);
    sinLatRad=sin(latr*pi/180);
    sinLongRad=sin(longr*pi/180);
    loci = GpsToECEF( lati,  longi,  alti);
    locr = GpsToECEF( latr,  longr,  altr);

    dx = loci(:,1)-locr(:,1); dy = loci(:,2)-locr(:,2); dz = loci(:,3)-locr(:,3);

    e= dx.*(-sinLongRad)+dy*(cosLongRad);
    n= dx.*(-sinLatRad).*(cosLongRad)+dy.*(-sinLatRad).*(sinLongRad)+dz.*cosLatRad;
    u= dx.*(cosLatRad).*(cosLongRad)+dy.*(cosLatRad).*(sinLongRad)+dz.*sinLatRad;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
function out = GpsToECEF( lat,  long,  alt)
     %input alt in meters, out in km
     lat = lat*pi/180; long = long*pi/180;
     a =6378.1;
     b =6356.8;
     e = 1-(b^2/a^2);
     N = a./(sqrt(1.0-(e.*power(sin(lat),2))));
     cosLatRad = cos(lat);
     cosLongiRad = cos(long);
     sinLatRad = sin(lat);
     sinLongiRad = sin(long);
     x =(N+0.001*alt).*cosLatRad.*cosLongiRad;
     y =(N+0.001*alt).*cosLatRad.*sinLongiRad;
     z =((power(b, 2)./power(a, 2)).*N+0.001*alt).*sinLatRad;
    
    out = [x y z];
end
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
function out = read_EI_data(filename)
    data = readcell(filename);
    data(cellfun('isempty',data)) = {NaN};
    [N,d] = size(data);
    %get 2022 data after discarding the first row that has the labels
    i = find([data{2:end,13}]==2022); i = i+1;
    data = data(i,:);
    
    RNid = data{1,1}; p_distinct = str2num(RNid(3:end));           % get plant ID
    cnt = 1; d_distinct = []; 
    %gather data for distinct stacks
    while (size(data,1)) 
        RNid = data{1,1};  tid = str2num(RNid(3:end));                                          % get plant ID
        if isempty(find(p_distinct==tid))
            p_distinct = [p_distinct;tid];
        end
        sid  = data{1,10};                                         % get stack ID
        EPNid(cnt,1:length(sid)) = sid; cnt = cnt+1;          
        d_distinct = [d_distinct ;tid extract_stack_data(data)];
        ri = cellfun(@(x) strcmp(sid, x), data(:,10));             % discard duplicates
        data = data(find(~ri),:);                                                                 
    end
    
    %keep stacks that have effective heat_out >= 5 MW
    ind = find(d_distinct(:,1)==p_distinct(1) & d_distinct(:,4).*d_distinct(:,6) >= 5);
    out.p1 = d_distinct(ind,:); %first one is Air Liq
    ind = find(d_distinct(:,1)~=p_distinct(1) & d_distinct(:,4).*d_distinct(:,6) >= 5);
    out.p2 = d_distinct(ind,:); %the rest are at P2 site
  
end
    
function out = extract_stack_data(in)
    ophr_frac = [in{1,9}]'/8760; 			% fraction of operating hours
    yr = [in{1,13}]';				    	% year
    lat = [in{1,19}]'; 			       	% latitude
    lon = [in{1,20}]'; 			    	% longitude
    D = [in{1,21}]'*0.3048;  				% diameter ft to m
    T = (5/9)*([in{1,23}]'-32)+273.15; 	% Temp F to K  
    w = [in{1,24}]'*0.3048;  				% velocity ft/s to m/s
    T0 = 293; 						        % env temperature in K
    po = 1.01325e5; 				    	% pressure in Pa
    Ra = 287; 						        % J/kg/K
    cpa = 1004; 				        	% J/kg/K
    rho = po./(Ra*T);
    heat_out = rho.*cpa.*(pi*D.^2/4).*w.*(T - T0)*1e-6; % MW
    out = [lat lon heat_out yr ophr_frac D T w];
end