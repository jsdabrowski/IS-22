package com.vogella.com.vogella.maven.eclipse;

import static org.junit.Assert.*;
import org.junit.Test;

import java.io.FileInputStream;
import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import static java.time.temporal.ChronoUnit.SECONDS;

public class DataManipulationTestCases {
	
	@Test
	public void TestFileCreated() {
		
		String pathname = "/Users/jacekdabrowski/Desktop/my-phd/Files-experiments-search/";
		String filename = "results_lucene_search.xlsx";
		
		XlsManipulation XMLfile = new XlsManipulation();
		
		assertTrue(XMLfile.CreateFile(pathname,filename));	

	}
	
	@Test
	public void TestReadFile() {
		
		String pathname = "/Users/jacekdabrowski/Desktop/my-phd/Files-experiments-search/";
		String filename = "eBay_500.xlsx";
		int numberReviews = 50;
		
		XlsManipulation XMLfile = new XlsManipulation();
		List<Review> listAppReviews = XMLfile.readFile(pathname, filename, numberReviews);
		
	    Iterator <Review> iterator = listAppReviews.iterator();
	    while(iterator.hasNext()) {
	    	
	    	Review AppReview = iterator.next();
	    	System.out.println(AppReview.getAppId());
	    	System.out.println(AppReview.getReviewId());
	    	System.out.println(AppReview.getContent());
	    			
	    }
		
	}
	
	@Test
	public void TestFileAppended()  throws Throwable {
		
		String pathname = "/Users/jacekdabrowski/Desktop/my-phd/Files-experiments-search/";
		String filename = "results_lucene_search.xlsx";
		
		// Testing appending reviews to xls file.
		List<Review> AppReviews = new ArrayList<Review>();
		
		Review ExamplaryAppReview = new Review();
		ExamplaryAppReview.setAppId("app_123");
		ExamplaryAppReview.setContent("this is the first review");
		ExamplaryAppReview.setOrginalQuery("query_1");
		ExamplaryAppReview.setProcessedQuery("query 1 proces");
		ExamplaryAppReview.setReviewId("rev_1");
		ExamplaryAppReview.setSimilarity(1);
		
		Review ExamplaryAppReview2 = new Review();
		ExamplaryAppReview2.setAppId("app_123");
		ExamplaryAppReview2.setContent("this is the second review");
		ExamplaryAppReview2.setOrginalQuery("query_1");
		ExamplaryAppReview2.setProcessedQuery("query 1 proces");
		ExamplaryAppReview2.setReviewId("rev_2");
		ExamplaryAppReview2.setSimilarity(1);

		Review ExamplaryAppReview3 = new Review();
		ExamplaryAppReview3.setAppId("app_123");
		ExamplaryAppReview3.setContent("this is the third review");
		ExamplaryAppReview3.setOrginalQuery("query_1");
		ExamplaryAppReview3.setProcessedQuery("query 1 proces");
		ExamplaryAppReview3.setReviewId("rev_3");
		ExamplaryAppReview3.setSimilarity(1);
		
		AppReviews.add(ExamplaryAppReview);
		AppReviews.add(ExamplaryAppReview2);
		AppReviews.add(ExamplaryAppReview3);

		XlsManipulation XMLfile = new XlsManipulation();
		
		assertTrue(XMLfile.AppendFile(pathname, filename, AppReviews));
	}	

	
}
