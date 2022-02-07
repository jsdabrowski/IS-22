package com.vogella.com.vogella.maven.eclipse;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.NumericDocValuesField;
import org.apache.lucene.document.SortedDocValuesField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.search.similarities.BM25Similarity;
import org.apache.lucene.search.similarities.BasicModelIn;
import org.apache.lucene.search.similarities.BasicModelIne;
import org.apache.lucene.search.similarities.BooleanSimilarity;
import org.apache.lucene.search.similarities.ClassicSimilarity;
import org.apache.lucene.search.similarities.LambdaTTF;
import org.apache.lucene.store.Directory;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.search.IndexSearcher;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

//Container for storing hit documents, their id and similarity measure
class hitDocumentsContainer {
	
    private TopFieldDocs topDocs;
    private List<Document> documents;
    
    public hitDocumentsContainer(TopFieldDocs topDocs, List<Document> documents) {
    		this.topDocs = topDocs;
    		this.documents = documents;
    }
    
    public TopDocs getTopDocs() {
    		return this.topDocs;
    	}
    
    public List<Document> getDocuments(){
		return this.documents;
    }

}
	

// Class for indexing and manipulating documents in the memory
public class InMemoryLuceneIndex {
	
	// Documents indexed in the memory instead of external directory
	// An abstraction layer for storing a list of files
	private Directory memoryIndex;
	
    // Initializing English Analyzer for indexed documents and queries 
	private EnglishAnalyzer analyzer;

	// Instantiate MemoryIndex and Analyzer 
    public InMemoryLuceneIndex(Directory memoryIndex, EnglishAnalyzer analyzer) {
        this.memoryIndex = memoryIndex;
        this.analyzer = analyzer;
    }

    // Create and index a document in the memory
    public void indexDocument(String reviewNo, String appId, String reviewId, String content) {
        IndexWriterConfig indexWriterConfig = new IndexWriterConfig(analyzer);
        try {
        	
        		// Creates and maintains an index (IndexWriter)
            IndexWriter writter = new IndexWriter(memoryIndex, indexWriterConfig);
            
            // Create new document
            Document document = new Document();
            document.add(new TextField("reviewNo", reviewNo, Field.Store.YES));
            document.add(new TextField("appId", appId, Field.Store.YES));
            document.add(new TextField("reviewId", reviewId, Field.Store.YES));
            document.add(new TextField("content", content, Field.Store.YES));
           
            //TODO Likely remove later
//            document.add(new SortedDocValuesField("reviewNo", new BytesRef(reviewNo)));

            writter.addDocument(document);
            writter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    
    // Search and return N-Top Documents
    // Adopt BM25 Similarity Measure
    // Boolean Query With QueryPhrase and MatchAllTheDocuments 
    
    public hitDocumentsContainer searchIndex(String inField, String queryString, int topNumber) {

        try {
        	
        		// Set Field for Search and Analyzer for Processing the Query
            Query query = new QueryParser(inField, analyzer).parse(queryString);

            Query queryMatchAllDocsQuery = new MatchAllDocsQuery();

            BooleanQuery booleanQuery 
              = new BooleanQuery.Builder()
                .add(query, BooleanClause.Occur.SHOULD)
                .add(queryMatchAllDocsQuery,BooleanClause.Occur.SHOULD)
                .build();
            
            // Open existing index
            IndexReader indexReader = DirectoryReader.open(memoryIndex);
            
            // Build Search Engine
            IndexSearcher searcher = new IndexSearcher(indexReader);
            
            // Set Similarity Measure
            // BM25Similarity; ClassicSimilarity; BooleanSimilarity
            searcher.setSimilarity(new BM25Similarity());
            
            // Match and Return 10-Top Documents for Given Query
            TopFieldDocs topDocs = searcher.search(booleanQuery, topNumber, Sort.RELEVANCE, true, false);

            // Container of hit documents' fields 
            List<Document> documents = new ArrayList<>();
            
            for (ScoreDoc scoreDoc : topDocs.scoreDocs) {

                documents.add(searcher.doc(scoreDoc.doc));
            }
            
            // CustomContainer for Storing Documents, their id and sim_measure
            hitDocumentsContainer containerDocuments = 
            		new hitDocumentsContainer(topDocs, documents);

            	  return containerDocuments;   	
            
        } catch (IOException | ParseException e) {
            e.printStackTrace();
        }
        return null;
    }
  
}
