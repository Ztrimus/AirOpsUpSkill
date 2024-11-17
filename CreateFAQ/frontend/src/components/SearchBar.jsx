import React, { useState, useEffect } from 'react';

const SearchBar = ({ onSearch }) => {
	const [query, setQuery] = useState('');
	const [debouncedQuery, setDebouncedQuery] = useState('');

	// Debounce effect to minimize API calls
	useEffect(() => {
		const handler = setTimeout(() => {
			setDebouncedQuery(query);
		}, 300);

		return () => {
			clearTimeout(handler);
		};
	}, [query]);

	// Trigger the search when the debounced query changes
	useEffect(() => {
		if (debouncedQuery.trim() !== '') {
			onSearch(debouncedQuery);
		} else {
			onSearch('');
		}
	}, [debouncedQuery, onSearch]);

	return (
		<div className='flex w-full h-12'>
			<input
				type='text'
				placeholder='Search FAQs by question or answer...'
				className='flex-grow border border-gray-300 rounded-l-md px-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400'
				value={query}
				onChange={(e) => setQuery(e.target.value)}
			/>
			<button
				className='bg-black text-white px-6 rounded-r-md hover:bg-gray-700 text-sm'
				onClick={() => onSearch(query)}
				disabled={!query.trim()}
			>
				Search
			</button>
		</div>
	);
};

export default SearchBar;
