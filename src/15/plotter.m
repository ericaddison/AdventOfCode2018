clc
clear all
close all

for x = 0:102
  file = ['./out/map', num2str(x)];
  map{x+1} = load(file);
end

for y = 1:5
  for x = 1:103
    imagesc(map{x})
    pause(0.1)
  end
end