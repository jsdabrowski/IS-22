package com.vogella.com.vogella.maven.eclipse;

import java.util.Comparator;

public class Review {
	
	private String reviewNo;
	private String appId;
	private String reviewId;
	private String content;
	private String orginalQuery;
	private String processedQuery;
	private float similarity;

	public void setAppId(String cellValue) {
		// TODO Auto-generated method stub
		this.appId = cellValue;
	}

	public void setReviewId(String cellValue) {
		// TODO Auto-generated method stub
		this.reviewId = cellValue;
		
	}

	public void setContent(String cellValue) {
		// TODO Auto-generated method stub
		this.content = cellValue;
		
	}

	public void setOrginalQuery(String cellValue) {
		// TODO Auto-generated method stub
		this.orginalQuery = cellValue;
	}

	public void setProcessedQuery(String cellValue) {
		// TODO Auto-generated method stub
		this.processedQuery = cellValue;
	}

	public void setSimilarity(float cellValue) {
		// TODO Auto-generated method stub
		this.similarity = cellValue;
		
	}
	
	public void setReviewNo(String cellValue) {
		this.reviewNo = cellValue;
	}

	public String getAppId() {
		return this.appId;
	}

	public String getReviewId() {
		return this.reviewId;
	}

	public String getContent() {
		return this.content;
	}
	
	public String getOrginalQuery() {
		return this.orginalQuery;
	}
	
	public String getProcessedQuery() {
		return this.processedQuery;
	}

	public float getSimilarity() {
		return this.similarity;
	}
	
	public String getReviewNo() {
		return this.reviewNo;
	}

}

class sortByReviewNo implements Comparator<Review>
{
    // Used for sorting in ascending order of
    // roll number
    public int compare(Review a, Review b)
    {
        return Integer.parseInt(a.getReviewNo()) - Integer.parseInt(b.getReviewNo());
    }
}
