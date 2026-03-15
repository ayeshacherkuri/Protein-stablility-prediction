import { clsx } from 'clsx';
// Since we didn't install tailwind-merge (as per plan to avoid tailwind unless requested), 
// we'll just use clsx for now. 
// If using pure CSS modules, standard className concat is fine, but clsx handles conditionals well.

export function cn(...inputs) {
    return clsx(inputs);
}
