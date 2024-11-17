import React, { useState } from 'react';
import FAQList from './components/FAQList';
import SearchBar from './components/SearchBar';

const App = () => {
	const [searchQuery, setSearchQuery] = useState('');

	return (
		<div className='container mx-auto p-4'>
			<h1 className='text-2xl font-bold mb-4'>CreateFAQ System</h1>
			<SearchBar onSearch={(query) => setSearchQuery(query)} />
			<FAQList searchQuery={searchQuery} />
		</div>
	);
};

export default App;
