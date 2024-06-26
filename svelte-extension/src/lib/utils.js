// @ts-nocheck
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { cubicOut } from "svelte/easing";

export function cn(...inputs) {
	return twMerge(clsx(inputs));
}

export const flyAndScale = (
	node,
	params = { y: -8, x: 0, start: 0.95, duration: 150 }
) => {
	const style = getComputedStyle(node);
	const transform = style.transform === "none" ? "" : style.transform;

	const scaleConversion = (valueA, scaleA, scaleB) => {
		const [minA, maxA] = scaleA;
		const [minB, maxB] = scaleB;

		const percentage = (valueA - minA) / (maxA - minA);
		const valueB = percentage * (maxB - minB) + minB;

		return valueB;
	};

	const styleToString = (style) => {
		return Object.keys(style).reduce((str, key) => {
			if (style[key] === undefined) return str;
			return str + `${key}:${style[key]};`;
		}, "");
	};

	return {
		duration: params.duration ?? 200,
		delay: 0,
		css: (t) => {
			const y = scaleConversion(t, [0, 1], [params.y ?? 5, 0]);
			const x = scaleConversion(t, [0, 1], [params.x ?? 0, 0]);
			const scale = scaleConversion(t, [0, 1], [params.start ?? 0.95, 1]);

			return styleToString({
				transform: `${transform} translate3d(${x}px, ${y}px, 0) scale(${scale})`,
				opacity: t
			});
		},
		easing: cubicOut
	};
};

export const isValidStockSymbol = (str) => {
	// Check if the string is empty or undefined
	if (!str) {
	  return false;
	}
  
	// Regular expression to match valid stock symbol format
	const regex = /^[A-Z][A-Z0-9]{1,4}$/;
  
	// Return true if the string matches the regex, false otherwise
	return regex.test(str);
}

export const queryStockData = async (symbol, length, timeseries="WEEKLY") => {
	const base_url = "https://65f7764db2fafbd9238d.appwrite.global"

	try {

		// Replace 'your_api_url' with the actual URL for your stock data API
		const response = await fetch(`${base_url}/stocks?symbol=${symbol}&timeseries=${timeseries}&length=${length}`);

		console.log(response)
	
		if (!response.ok) {
			throw new Error(`Error fetching data: ${response.status} ${symbol}`);
		}
	
		const data = await response.json();
		
		if (data.error) {
			throw new Error(data.error);
		}
	
		return data.documents;
	} catch (error) {
		console.error("Error retrieving stock data:", error);
		return []; // Return an empty array on error
	}
}

export function calculatePercentChange(currentPrice, pastPrice) {
	const percentChange = ((currentPrice - pastPrice) / pastPrice) * 100;
	return percentChange.toFixed(2); // Round the result to 2 decimal places
}