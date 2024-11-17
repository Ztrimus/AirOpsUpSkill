import React, { useEffect, useState } from 'react';
import axios from 'axios';
import FAQCard from './FAQCard';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import SearchBar from './SearchBar';

const FAQList = () => {
	const [faqs, setFaqs] = useState([]);
	const [machineTypes, setMachineTypes] = useState([]);
	const [loading, setLoading] = useState(true);
	const [searchQuery, setSearchQuery] = useState('');
	const [filters, setFilters] = useState({
		machine_type: '',
		sortBy: '',
	});
	const [currentPage, setCurrentPage] = useState(1);

	const fetchMachineTypes = async () => {
		try {
			const { data } = await axios.get('http://localhost:8000/repairjobs/machine-types');
			setMachineTypes(data);
		} catch (error) {
			console.error('Error fetching machine types:', error);
			toast.error('Failed to load machine types.');
		}
	};

	const fetchFAQs = async () => {
		try {
			setLoading(true);
			const { data } = await axios.get('http://localhost:8000/faqs', {
				params: { ...filters, searchQuery, page: currentPage },
			});
			setFaqs(data);
		} catch (error) {
			console.error('Error fetching FAQs:', error);
			toast.error('Failed to load FAQs.');
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		fetchMachineTypes();
		fetchFAQs();
	}, [filters, searchQuery, currentPage]);

	const handleFeedback = async (faqId, feedbackType) => {
		try {
			await axios.post('http://localhost:8000/faqs/feedback', {
				faq_id: faqId,
				rating: feedbackType === 'helpful' ? 1 : -1,
				feedback: feedbackType,
			});
			toast.success('Thank you for your feedback!');
		} catch (error) {
			console.error('Error submitting feedback:', error);
			toast.error('Error submitting feedback. Please try again.');
		}
	};

	const createFAQ = async () => {
		try {
			await axios.post('http://localhost:8000/generate-faqs');
			toast.success('FAQs generated successfully!');
			fetchFAQs(); // Refresh FAQs
		} catch (error) {
			console.error('Error generating FAQs:', error);
			toast.error('Error generating FAQs.');
		}
	};

	if (loading) return <p>Loading FAQs...</p>;

	return (
		<div className='container mx-auto px-4 py-8'>
			<ToastContainer />
			<div className='space-y-4'>
				{/* Title and Button */}
				<div className='flex flex-col md:flex-row md:justify-between md:items-center'>
					<h1 className='text-4xl font-bold tracking-tight'>
						Frequently Asked Questions
					</h1>
					{/* <button
						className='bg-black text-white px-4 py-2 rounded-md hover:bg-gray-700'
						onClick={createFAQ}
					>
						Generate FAQs
					</button> */}
				</div>

				{/* Filters */}
				<div className='flex flex-col md:flex-row md:items-center gap-4'>
					<select
						className='h-12 border border-gray-300 rounded-md px-3'
						onChange={(e) =>
							setFilters((prev) => ({ ...prev, machine_type: e.target.value }))
						}
					>
						<option value=''>All Machines</option>
						{machineTypes.map((type, index) => (
							<option key={index} value={type}>
								{type}
							</option>
						))}
					</select>

					<select
						className='h-12 border border-gray-300 rounded-md px-3'
						onChange={(e) =>
							setFilters((prev) => ({ ...prev, sortBy: e.target.value }))
						}
					>
						<option value=''>Sort By</option>
						<option value='rating_desc'>Highest Rated</option>
						<option value='rating_asc'>Lowest Rated</option>
						<option value='newest'>Newest First</option>
						<option value='oldest'>Oldest First</option>
					</select>
					<SearchBar onSearch={(query) => setSearchQuery(query)} />
				</div>

				{/* FAQ Cards */}
				<div className='grid gap-6 md:grid-cols-2 lg:grid-cols-3'>
					{faqs.length > 0 ? (
						faqs.map((faq) => (
							<FAQCard
								key={faq.faq_id}
								faq_name={faq.faq_name}
								machine_type={faq.machine_type}
								common_3_repairs={faq.common_3_repairs}
								common_3_culprits={faq.common_3_culprits}
								solution_to_single_frequent_culprit={
									faq.solution_to_single_frequent_culprit
								}
								rating={faq.rating || 0}
								onFeedback={(type) => handleFeedback(faq.faq_id, type)}
							/>
						))
					) : (
						<p>No FAQs found for your query.</p>
					)}
				</div>

				{/* Pagination */}
				<div className='flex justify-center mt-4'>
					<button
						className='btn btn-outline mr-2'
						disabled={currentPage === 1}
						onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
					>
						Previous
					</button>
					<span>Page {currentPage}</span>
					<button
						className='btn btn-outline ml-2'
						onClick={() => setCurrentPage((prev) => prev + 1)}
					>
						Next
					</button>
				</div>
			</div>
		</div>
	);
};

export default FAQList;
