// src/components/IconComponent.tsx
import React from 'react';

// Define available icon types
export type IconName = 'sun' | 'moon';

// Props for our icon component
interface IconComponentProps {
  name: IconName;
  size?: number;
  color?: string;
  className?: string;
}

// Custom icon component that uses inline SVG
const IconComponent: React.FC<IconComponentProps> = ({ 
  name, 
  size = 20, 
  color = 'currentColor',
  className = '' 
}) => {
  // SVG path data for different icons
  const iconPaths: Record<IconName, string> = {
    sun: 'M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42M17 12a5 5 0 11-10 0 5 5 0 0110 0z',
    moon: 'M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z'
  };
  
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={`feather ${className}`}
    >
      <path d={iconPaths[name]} />
    </svg>
  );
};

export default IconComponent;