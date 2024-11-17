import React, { useState } from 'react';
import FAQList from './components/FAQList';
import './BackgroundEffect.css'; // Import the background effect CSS
import SearchBar from './components/SearchBar';

const App = () => {
	const [searchQuery, setSearchQuery] = useState('');

	return (
		<div className='app'>
			{/* Background Layers */}
			<div className='bg'></div>
			<div className='bg bg2'></div>
			<div className='bg bg3'></div>

			{/* Content Area */}
			<div className='content'>
				<FAQList searchQuery={searchQuery} />
			</div>
		</div>
	);
};

export default App;
