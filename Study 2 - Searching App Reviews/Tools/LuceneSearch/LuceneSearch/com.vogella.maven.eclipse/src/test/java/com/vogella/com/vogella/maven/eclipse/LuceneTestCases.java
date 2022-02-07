package com.vogella.com.vogella.maven.eclipse;

import static org.junit.Assert.*;
import org.junit.Test;

import java.util.List;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.LowerCaseFilter;
import org.apache.lucene.analysis.StopFilter;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.MatchAllDocsQuery;
import org.apache.lucene.search.PhraseQuery;
import org.apache.lucene.search.PrefixQuery;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.search.WildcardQuery;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.BytesRef;
import java.util.Iterator;

public class LuceneTestCases {

	@Test
	public void givenSearchQueryWhenFetchedDocumentThenCorrect() {
		
	    // Create index in the memory
		InMemoryLuceneIndex inMemoryLuceneIndex 
	      = new InMemoryLuceneIndex(new RAMDirectory(), new EnglishAnalyzer());
				
		// Store and index documents 
		inMemoryLuceneIndex.indexDocument("1", "whatsapp", "123", "hello some world 3");
		inMemoryLuceneIndex.indexDocument("2", "skype", "321", "Some hello world");
	    inMemoryLuceneIndex.indexDocument("3", "whatsapp","123-sd", "Some hello worlds 2");
		inMemoryLuceneIndex.indexDocument("4", "skype", "123-sdsd", "It is very strange worlds");
		inMemoryLuceneIndex.indexDocument("5", "whatsapp", "321-sd", "Buying and selling items on the go has never been easier. This apps seamless platform allows for quick detailed searches, easy bidding and great notifications.");
		inMemoryLuceneIndex.indexDocument("4", "skype", "3213-s", "Makes it so much easier to connect to E-Bay than having to type it in to a search engine. It's great!!");
		
		
	    // Search and return N-top documents
	    // BM25 Similarity Measure 
			
		int topNumber = 10;
	    hitDocumentsContainer documents = 
	    		inMemoryLuceneIndex.searchIndex("content", "search item", topNumber);
	    
	    // Print the number of hits and the content of these documents
	    System.out.printf("The number of hits: %d \n", documents.getTopDocs().totalHits);

	    // Print document's position, content and similarity measure
	    for (int i = 0; i < documents.getTopDocs().totalHits; i++) {
	    	
		    	System.out.println("Document id: " + documents.getTopDocs().scoreDocs[i].doc);
//		    	System.out.println("Document app id: " +  documents.getDocuments().get(i).get("appId"));
		    	System.out.println("Document review no: " +  documents.getDocuments().get(i).get("reviewNo"));
//		    	System.out.println("Document reviewNo: " +  documents.getDocuments().get(i).get("reviewNo"));
		    	System.out.println("Document content: " +  documents.getDocuments().get(i).get("content"));
	 	    	System.out.println("Document similarity: " + documents.getTopDocs().scoreDocs[i].score);
	    }
	    	   
	    assertEquals("Some hello world",documents.getDocuments().get(0).get("content"));
	}
	
}

	
