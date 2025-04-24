import React, { useState, useEffect } from 'react';
import { FaSearch, FaMicrophone } from 'react-icons/fa';

const SearchBar = ({ onSearch }) => {
	const [query, setQuery] = useState('');
	const [debouncedQuery, setDebouncedQuery] = useState('');

	// // Debounce effect to minimize API calls
	// useEffect(() => {
	// 	const handler = setTimeout(() => {
	// 		setDebouncedQuery(query);
	// 	}, 300);

	// 	return () => {
	// 		clearTimeout(handler);
	// 	};
	// }, [query]);

	// // Trigger the search when the debounced query changes
	// useEffect(() => {
	// 	if (debouncedQuery.trim() !== '') {
	// 		onSearch(debouncedQuery);
	// 	} else {
	// 		onSearch('');
	// 	}
	// }, [debouncedQuery, onSearch]);

	return (
		<div className='flex w-full h-12'>
			{/* Input Field */}
			<input
				type='text'
				placeholder='Search FAQs by question or answer...'
				className='flex-grow border border-gray-300 rounded-l-md px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400'
				value={query}
				onChange={(e) => setQuery(e.target.value)}
			/>

			{/* Button Container */}
			<div className='bg-black text-white px-4 flex items-center rounded-r-md'>
				{/* Microphone Icon */}
				<button className='mr-4 focus:outline-none'>
					<FaMicrophone size={16} />
				</button>

				{/* Search Icon */}
				<button
					className='focus:outline-none'
					onClick={() => onSearch(query)}
					disabled={!query.trim()}
				>
					<FaSearch size={16} />
				</button>
			</div>
		</div>
	);
};

export default SearchBar;
