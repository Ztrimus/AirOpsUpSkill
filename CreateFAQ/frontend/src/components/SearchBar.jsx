/*
 * -----------------------------------------------------------------------
 * File: frontend/SearchBar.jsx
 * Creation Time: Nov 16th 2024, 8:07 pm
 * Author: Saurabh Zinjad
 * Developer Email: saurabhzinjad@gmail.com
 * Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
 * -----------------------------------------------------------------------
 */

import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
	const [query, setQuery] = useState('');

	const handleSearch = (e) => {
		e.preventDefault();
		onSearch(query);
	};

	return (
		<form className='flex gap-2 my-4' onSubmit={handleSearch}>
			<input
				type='text'
				placeholder='Search FAQs...'
				className='input input-bordered w-full'
				value={query}
				onChange={(e) => setQuery(e.target.value)}
			/>
			<button type='submit' className='btn btn-primary'>
				Search
			</button>
		</form>
	);
};

export default SearchBar;
