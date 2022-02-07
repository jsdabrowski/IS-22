package com.vogella.com.vogella.maven.eclipse;

import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.store.RAMDirectory;
import org.junit.Test;

/*
 * The test class responsible for the overall experiment execution 
 */

	// Step 1: Read Reviews From xls File +
	// Step 2: Execute Searching for Given Queries +
	// Step 3: Create File for Reviews +
	// Step 4: Save Results in the File +

public class TotalExperimentTestCases {
		    
	// Location of a xls file with app reviews
	private String inputPathname = "/Users/jacekdabrowski/Desktop/Collected reviews/";
	private String inputFilename = "Evernote_1250_review_level.xlsx";
	int numberReviews = 1250;
	
	private String outputPathname = "/Users/jacekdabrowski/Desktop/";
	private String outputFilename = "results_lucene_search_";
	
	// Input queries 
	private List<String> orginalQueries = Arrays.asList("Create shortcuts", "Write notes");

	@Test
	public void executeExperiment() {
		
		Instant start = Instant.now();
		
		//Step 1: Read Reviews From xls File
		XlsManipulation XMLfile = new XlsManipulation();
		List<Review> listAppReviews = XMLfile.readFile(inputPathname, inputFilename, numberReviews);
		
		// Create Lucene's index in the memory
		InMemoryLuceneIndex inMemoryLuceneIndex = new InMemoryLuceneIndex(new RAMDirectory(), new EnglishAnalyzer());
					
		// Store and index each app review 
	    Iterator <Review> iterator = listAppReviews.iterator();
	    int totalReviewNo = listAppReviews.size();
	    int currentReview = 0;
	    		
	    while(iterator.hasNext()) {
	    	
		    	Review AppReview = iterator.next();
		    	currentReview += 1;
		    	inMemoryLuceneIndex.indexDocument(String.valueOf(currentReview),AppReview.getAppId(), AppReview.getReviewId(), AppReview.getContent());

	    }
	  
		// For each query perform the experiment and save the result 
		Iterator <String> iteratorQuery = orginalQueries.iterator();
		
		while(iteratorQuery.hasNext()) {
			
		    	String query = iteratorQuery.next();
		  
		    // Search and return N-top documents based on BM25 Measure 
				
			int topNumber = listAppReviews.size();
			
			hitDocumentsContainer documents = 
		    		inMemoryLuceneIndex.searchIndex("content", query, topNumber);
		    
		    // Append to Each Review Information about Query and Similarity Score 
		    List<Review> listAppReviewsRefined = new ArrayList<>();
		    // TODO Below line likely remove
//	    		Iterator <Review> iteratorRefined = listAppReviews.iterator();

	    		for (int i = 0; i < documents.getTopDocs().totalHits; i++) {
			    	
	    			Review AppReviewRefined = new Review();
	    			
	    			AppReviewRefined.setReviewNo(documents.getDocuments().get(i).get("reviewNo"));
	    			AppReviewRefined.setAppId(documents.getDocuments().get(i).get("appId"));
	    			AppReviewRefined.setReviewId(documents.getDocuments().get(i).get("reviewId"));
	    			AppReviewRefined.setContent(documents.getDocuments().get(i).get("content"));
	    			AppReviewRefined.setSimilarity(documents.getTopDocs().scoreDocs[i].score);
	    			AppReviewRefined.setOrginalQuery(query);;

	    			listAppReviewsRefined.add(AppReviewRefined);
	    			
			    }
	    		
	    		Collections.sort(listAppReviewsRefined, new sortByReviewNo());
	    		
	    		// TODO Below code likely remove
//		    for (int i = 0; i < documents.getTopDocs().totalHits; i++) {
//
//		    		if(iteratorRefined.hasNext()) {
//		    			 			
//		    			Review AppReviewRefined = iteratorRefined.next();
//		    			
//		    			AppReviewRefined.setOrginalQuery(query);
//		    			AppReviewRefined.setSimilarity(documents.getTopDocs().scoreDocs[i].score);
//		    			listAppReviewsRefined.add(AppReviewRefined);
//
//		    			
//			    	}
//		    
//		    }
		    
		    // TODO Below prints could be removed or commented
		    
		    // Print the query
		    System.out.printf("Query: " + query + "\n");

		    // Print the number of hits and the content of these documents
		    System.out.printf("The number of hits: %d \n", documents.getTopDocs().totalHits);

		    // Print document's position, content and similarity measure
		    for (Review AppReview : listAppReviewsRefined) {
		    	
			    	System.out.println("Review no: " + AppReview.getReviewNo());
			    	System.out.println("App id: " + AppReview.getAppId());
			    	System.out.println("Review id: " + AppReview.getReviewId());
			    	System.out.println("Content: " + AppReview.getContent());
			    	System.out.println("Similarity: " + AppReview.getSimilarity());

		    }

		 	// Step 3: Create File for Reviews 
		    	String outputFilename = this.outputFilename + "query_" + (orginalQueries.indexOf(query)+1) + "_" + query + ".xlsx";
		    	XMLfile.CreateFile(outputPathname,outputFilename);
		    	
		    	// Step 4: Save Results
		    	try {
					XMLfile.AppendFile(outputPathname, outputFilename, listAppReviewsRefined);
				} catch (IOException e) {
					// TODO Auto-generated catch block
					System.err.println("The result of the experiment could not be saved.");
					e.printStackTrace();
				}
		    
		    

		    	
	    	}
		
		System.out.println("The experiment took: " + Duration.between(start, Instant.now()));

	}
	
	
}
